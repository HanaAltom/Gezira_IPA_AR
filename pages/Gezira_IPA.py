#######################
import streamlit as st
from arabic_support import support_arabic_text
import pandas as pd
from shapely.geometry import Point
import geopandas as gpd
from streamlit_folium import st_folium
#######################
from util import common2 as cm
from util import Gezira_IPA_content_language as cl

logger = cm.logger

cm.set_page_container_style(
        max_width = 1100, max_width_100_percent = True,
        padding_top = 0, padding_right = 0, padding_left = 0, padding_bottom = 0
)

if "language" not in st.session_state or st.session_state.language == "a":
    support_arabic_text(all=True)
    lang = "a"
elif st.session_state.language == "e":
    support_arabic_text(all=False)
    lang = "e"
else:
    raise NotImplementedError("language not supported")

logo_small, logo_wide = cm.logos()

col = st.columns((5.5, 2.5), gap='small')
# Add a Reset Button as a Folium Marker
def reset_map():
    """Resets the selected polygon state."""
    st.session_state.selected_division = None
    st.rerun()



# Sidebar
with st.sidebar:

    st.logo(logo_wide, size="large", link='https://www.un-ihe.org/', icon_image=logo_small)

    if st.button("العربية"):
        st.session_state.language = "a"
        st.rerun()
    if st.button("English"):
        st.session_state.language = "e"
        st.rerun()

    st.title(cl.sidebar_title[lang])

    selected_crop_index = st.selectbox(
        cl.crop_lst["label"][lang],
        cl.crop_lst["values"]["index"],
        format_func=lambda x: cl.crop_lst["values"][lang][x],
    )
    selected_crop = cl.crop_lst["values"]["e"][selected_crop_index]
    dfm, geo = cm.read_df_and_geo(selected_crop)
    dfc = cm.read_crop_area_df()

    season_list = list(dfm.season.unique())[::-1]
    selected_season = st.selectbox(cl.select_season["label"][lang], season_list, index = 0,
                                 help=cl.select_season["help"][lang])
    st.write(cl.crop_calendar_txt(selected_crop_index, lang))

    ll = list(dfm.columns.unique())[3:][::-1]
    indicator_lst = cl.indicator_lst(ll)
    indicator_index = st.selectbox(
        indicator_lst["label"][lang],
        indicator_lst["values"]["index"],
        format_func=lambda x: indicator_lst["values"][lang][x],
        index=0,
        help=indicator_lst["help"][lang],
    )
    indicator = indicator_lst["values"]["e"][indicator_index]

    stats_lst = cl.stats_lst(list(cm.stat_dict.keys()))
    stats_index = st.selectbox(
        stats_lst["label"][lang],
        stats_lst["values"]["index"],
        format_func=lambda x: stats_lst["values"][lang][x],
        index=3,
        help=stats_lst["help"][lang],
    )
    selected_stat = stats_lst["values"]["e"][stats_index]
    selected_stat_abbr = cm.stat_dict[selected_stat]

    selected_indicator = f"{selected_stat_abbr}_{indicator.replace(' ', '_')}"

    st.write(f'{cm.IPA_description[indicator]}')
    stat_description = cm.stat_dict[selected_stat]

    df_selected = dfm[dfm.season == selected_season][[f'division_{lang}', selected_indicator]]
    df_selected_sorted = df_selected.sort_values(by=selected_indicator, ascending=False)

    #aggregate by divisions
    df_division = df_selected_sorted.groupby(f'division_{lang}').agg({selected_indicator:'mean'})#.rename(columns=d)
    df_division = df_division.sort_values(by=selected_indicator, ascending=False).reset_index()

    st.markdown("---")
    with st.expander(cl.about_the_map["label"][lang]):
        st.markdown(cl.about_the_map["markdown"][lang])

#######################
# Dashboard Main Panel

df_map = pd.DataFrame()
df_chart = pd.DataFrame()
col_name = ''
units = cm.units

# geopandas dataframe of the geo (AIO)
gdf = gpd.GeoDataFrame.from_features(geo['features'])

# Initialize session state
if "selected_division" not in st.session_state:
    st.session_state.selected_division = None
if "selected_section" not in st.session_state:
    st.session_state.selected_section = None

selected_year = int(selected_season.split('-')[1])
# Filter data based on selection
if st.session_state.selected_division is not None:
    # Add a reset button to Streamlit UI (works better than Folium custom HTML)
    selected_poly = st.session_state.selected_division
    filtered = [sgeo for sgeo in geo["features"] if sgeo['properties'][f'division_{lang}'] in selected_poly]

    filtered_geojson = {
        "type": "FeatureCollection",
        'name': 'test',#geo['name'],
        'crs': geo['crs'],
        "features": filtered
    }

    df_section = dfm[dfm.season == selected_season][[f'division_{lang}', f'section_{lang}', selected_indicator]]
    df_section =        df_section.sort_values(by=selected_indicator, ascending=False)
    df_section_division = df_section.loc[df_section[f'division_{lang}']==selected_poly]
    col_name = df_section_division.columns[1]
    geo2plot = filtered_geojson
    df_map = df_section_division
    dfm_var = dfm[['season',f'division_{lang}', f'section_{lang}',selected_indicator]]
    df_chart = dfm_var.loc[dfm_var[f'division_{lang}']==selected_poly]

    selected_sections_ids = [feature["properties"]['id'] for feature in filtered_geojson["features"]]
    dfca = dfc[(dfc['season'] == selected_year) & 
               (dfc['polygon_id'].isin(selected_sections_ids))].mean(numeric_only=True).to_frame().T.round(1)
else:
    col_name = df_division.columns[0]
    geo2plot = cm.merge_sections_to_divisions(geo, df_division, lang)
    df_map = df_division

    dfm_var = dfm[['season',f'division_{lang}', selected_indicator]].groupby(['season',f'division_{lang}'])
    df_chart = dfm_var.agg({selected_indicator:'mean'}).reset_index()

    dfca = dfc[dfc['season'] == selected_year].mean(numeric_only=True).to_frame().T.round(1)


choropleth = cm.make_folium_choropleth(geo2plot, selected_indicator, df_map, 
                                       col_name, lang)
line_chart, title = cm.make_alt_linechart(df_chart, selected_indicator, col_name, 
                                   selected_season, st.session_state.selected_section, lang)
title = f'<p style="font:Courier; color:gray; font-size: 20px;">{title}</p>'

if lang == "a":
    selected_name = 'الجزيرة'
else:
    selected_name = 'Gezira'
if st.session_state.selected_division is not None:
    selected_name = st.session_state.selected_division


# piechart = cm.crop_area_piechart(dfca)
piechart, titlepie = cm.plotly_pie_chart(dfca, selected_name, selected_year, lang)
titlepie = f'<p style="font:Courier; color:gray; font-size: 20px;">{titlepie}</p>'

with col[0]:
    # st.markdown('#####        Indicator Map')
    # st.markdown("<h4 style='text-align: center; color: white;'>Indicator Map</h4>", unsafe_allow_html=True)

    left, right = st.columns([0.7, 0.3])
    # left, right = st.columns((6, 2), gap='medium')
    with left:
        st.markdown(f"### {cl.indicator_map[lang]}")

    with right:
        # st.markdown("<br><br>", unsafe_allow_html=True) 
        st.markdown("<div style='margin-top: 12px;'>", unsafe_allow_html=True)
        if st.session_state.selected_division is not None:
            if st.button("🔄 Reset Map"):
                st.session_state.selected_section = None
                reset_map()

    map_data = st_folium(choropleth,  height=450, use_container_width=True)

    # st.write(map_data)
    st.write("")
    st.markdown(title, unsafe_allow_html=True)  
    st.altair_chart(line_chart, use_container_width=True)

    if map_data and "last_clicked" in map_data and map_data["last_clicked"] != None :
        # Find the clicked polygon
        clicked_point = Point(map_data["last_clicked"]["lng"], map_data["last_clicked"]["lat"])
        matching_polygon = gdf[gdf.contains(clicked_point)]
        if not matching_polygon.empty:
            clicked_division = matching_polygon.iloc[0][f'division_{lang}']
            clicked_section = matching_polygon.iloc[0][f'section_{lang}']
            if (st.session_state.selected_division != clicked_division) or (st.session_state.selected_section != clicked_section):
                    st.session_state.selected_division = clicked_division
                    st.session_state.selected_section = clicked_section
                    st.rerun()


with col[1]:
    # st.markdown('###### Bar chart of the selected indicator')
    # st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(titlepie, unsafe_allow_html=True)
    st.plotly_chart(piechart, use_container_width=True)
    chart, title  = cm.alt_bar_chart(df_map, selected_indicator, col_name, selected_season)
    title = f'<p style="font:Courier; color:gray; font-size: 20px;">{title}</p>'
    st.markdown(title, unsafe_allow_html=True)

    st.altair_chart(chart, use_container_width=True)


