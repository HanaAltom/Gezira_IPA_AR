from os.path import join
import streamlit as st
from streamlit_folium import st_folium

from util.common2 import (
    get_stats_arabic,
    get_stats_english,
    logos_and_language,
    read_dataset,
    read_df_and_geo,
)
from util.charts import alt_line_chart
from util.maps import (
    create_folium_map,
    extraxt_ts,
    filter_points_within_polygon,
    get_gdf_from_json,
)
from content.languages import arabic, english
from content.shared_content import (
    sidebar_title,
    select_season,
    select_indicator,
)
from content.raster_viewer_content import (
    raster_viewer_title,
    stats_table_title,
    about_raster_viewer,
    generate_time_series_button,
)


language: str = st.session_state.language

dfm, geo = read_df_and_geo('wheats')

gdf = get_gdf_from_json(geo)
ipa_ds_path = join("data", "Gezira_ipa_results.nc")

# Initialize session state
session_state_defaults = {
    'last_clicked': None,
    'clicked_locations': [],
    'time_series_generated': False,
    'button_clicked' : False
}
for key, default_value in session_state_defaults.items():
    if key not in st.session_state:
        st.session_state[key] = default_value


with st.sidebar:

    logos_and_language()

    st.title(sidebar_title[language])

    season_list = list(dfm.season.unique())[::-1]
    selected_season = st.selectbox(
        select_season["label"][language],
        season_list,
        index=0,
        help=select_season["help"][language],
    )
    assert isinstance(selected_season, str)

    ll = list(dfm.columns.unique())[3:][::-1]
    indicator_index = st.selectbox(
        select_indicator["label"][language],
        select_indicator["values"]["index"],
        format_func=lambda x: select_indicator["values"][language][x],
        index=0,
        help=select_indicator["help"][language],
    )
    indicator = select_indicator["values"][english][indicator_index]
    indicator_name = select_indicator["values"][language][indicator_index]
    unit = select_indicator["units"][language][indicator_index]

    st.markdown("---")

    with st.expander(about_raster_viewer["label"][language]):
        st.markdown(about_raster_viewer["markdown"][language])

variable = indicator.replace(' ', '_')
selected_time = selected_season.split('-')[1] # f'{selected_season}-12-31'

ds, transform, crs, nodata, bounds = read_dataset(ipa_ds_path)

# data =  ds.sel(time=slected_time)[variable]
data_var =  ds[variable]
data =  data_var.sel(season=int(selected_time)).load()

layout_columns = st.columns((5.5, 2.5), gap='small')

# right column
if language == arabic:
    df_stats = get_stats_arabic(data)
elif language == english:
    df_stats = get_stats_english(data)
else:
    raise NotImplementedError("language not supported")

with layout_columns[1]:
        st.write('')
        title = stats_table_title(indicator_name, unit, selected_season, language)
        title = f'<p style="font:Courier; color:gray; font-size: 20px;">{title}</p>'
        st.markdown(title, unsafe_allow_html=True)
        st.dataframe(df_stats, use_container_width=True)

with layout_columns[0]:
    st.markdown(f"### {raster_viewer_title[language]}: {selected_season}")
    # with st.spinner("Loading and processing data..."):
    #
    # Process clicked locations and display map

    if map_data := st_folium(create_folium_map(data, geo, bounds, crs, indicator_name, language),
                                height=500, width=None,
                                returned_objects=["last_clicked"]):

        # Process Click Event
        if map_data["last_clicked"] and map_data["last_clicked"] != st.session_state.last_clicked:
            lat, lon = map_data["last_clicked"]["lat"], map_data["last_clicked"]["lng"]

            if (lat, lon) not in st.session_state.clicked_locations:
                st.session_state.last_clicked = map_data["last_clicked"]
                st.session_state.clicked_locations.append((lat, lon))
                    # st.rerun()  # Rerun only when a new point is added

    filtered_markers = filter_points_within_polygon(st.session_state.clicked_locations, gdf)

    if len(filtered_markers) > 0 and not st.session_state.button_clicked:

        # st.markdown("---")
        if st.button(f"📈 {generate_time_series_button[language]}"):
            st.session_state.time_series_generated = True
            st.session_state.button_clicked = True
            st.rerun()

# **Display all extracted values**
locations = st.session_state.clicked_locations
if st.session_state.time_series_generated:
    data_all_points = extraxt_ts(data_var, locations)

    if(len(data_all_points) > 0):
        chart, title = alt_line_chart(
            data_all_points, variable, indicator_name, unit, language
        )
        title = f'<p style="font:Courier; color:gray; font-size: 20px;">{title}</p>'
        st.markdown(title, unsafe_allow_html=True)
        st.altair_chart(chart, use_container_width=True)
