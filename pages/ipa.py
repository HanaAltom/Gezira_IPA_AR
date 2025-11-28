import streamlit as st
import pandas as pd
from shapely.geometry import Point
import geopandas as gpd
from streamlit_folium import st_folium

from util.common2 import logos_and_language, read_df_and_geo
from util.charts import (
    alt_bar_chart, make_alt_linechart, plotly_pie_chart
)
from util.maps import (
    reset_map,
    make_folium_choropleth,
    merge_sections_to_divisions,
    read_crop_area_df,
)
from content.languages import english
from content.shared_content import (
    STATS,
    sidebar_title,
    select_season,
    select_indicator,
    select_stat,
)
from content.ipa_content import (
    indicator_map,
    select_crop_type,
    crop_calendar_txt,
    about_the_map,
    ipa_description,
    reset_map_label,
    pie_chart_name,
)


language: str = st.session_state.language

dfc = read_crop_area_df()

# Sidebar
with st.sidebar:
    logos_and_language()

    st.title(sidebar_title[language])

    selected_crop_index = st.selectbox(
        select_crop_type["label"][language],
        select_crop_type["values"]["index"],
        format_func=lambda x: select_crop_type["values"][language][x],
    )
    selected_crop = select_crop_type["values"][english][selected_crop_index]

    dfm, geo = read_df_and_geo(selected_crop)

    season_list = list(dfm.season.unique())[::-1]
    selected_season = st.selectbox(
        select_season["label"][language],
        season_list,
        index=0,
        help=select_season["help"][language],
    )
    assert isinstance(selected_season, str)
    st.write(crop_calendar_txt(selected_crop_index, language))

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

    stats_index = st.selectbox(
        select_stat["label"][language],
        select_stat["values"]["index"],
        format_func=lambda x: select_stat["values"][language][x],
        index=3,
        help=select_stat["help"][language],
    )
    selected_stat = select_stat["values"][english][stats_index]
    stat_name = select_stat["values"][language][stats_index]

    st.write(f'{ipa_description[indicator][language]}')

    st.markdown("---")
    with st.expander(about_the_map["label"][language]):
        st.markdown(about_the_map["markdown"][language])

#######################

# Dashboard Main Panel

# Initialize session state
if "selected_division" not in st.session_state:
    st.session_state.selected_division = None
if "selected_section" not in st.session_state:
    st.session_state.selected_section = None

# geopandas dataframe of the geo (AIO)
gdf = gpd.GeoDataFrame.from_features(geo['features'])

# Filter data based on selection
selected_indicator = f"{STATS[selected_stat]}_{indicator.replace(' ', '_')}"
selected_year = int(selected_season.split("-")[1])
selected_division = st.session_state.selected_division
df_season = dfm[dfm.season == selected_season][
    [
        "division",
        "section",
        f"division_{language}",
        f"section_{language}",
        selected_indicator,
    ]
]
assert isinstance(df_season, pd.DataFrame)
df_season = df_season.sort_values(by=selected_indicator, ascending=False)
if selected_division is not None:
    col_name = "section"
    # Add a reset button to Streamlit UI (works better than Folium custom HTML)
    filtered_features = [
        sgeo
        for sgeo in geo["features"]
        if sgeo["properties"]["division"] == selected_division
    ]

    geo2plot = {
        "type": "FeatureCollection",
        "name": "test",
        "crs": geo["crs"],
        "features": filtered_features,
    }

    df_map = df_season.loc[df_season["division"] == selected_division]
    dfm_var = dfm[
        [
            "season",
            "division",
            "section",
            f"division_{language}",
            f"section_{language}",
            selected_indicator,
        ]
    ]
    df_chart = dfm_var.loc[dfm_var["division"] == selected_division]

    selected_sections_ids = [
        feature["properties"]["id"] for feature in geo2plot["features"]
    ]
    s_c = dfc[
        (dfc["season"] == selected_year)
        & (dfc["polygon_id"].isin(selected_sections_ids))
    ].mean(numeric_only=True)

else:
    col_name = "division"
    # aggregate by divisions
    df_divisions = df_season.groupby("division").agg(
        {f"division_{language}": "first", selected_indicator: "mean"}
    )
    assert isinstance(df_divisions, pd.DataFrame)
    df_divisions = df_divisions.sort_values(
        by=selected_indicator, ascending=False
    ).reset_index()

    geo2plot = merge_sections_to_divisions(geo, df_divisions, language)
    df_map = df_divisions

    dfm_var = dfm[["season", "division", f"division_{language}", selected_indicator]].groupby(
        ["season", "division"]
    )
    df_chart = dfm_var.agg(
        {f"division_{language}": "first", selected_indicator: "mean"}
    ).reset_index()

    assert isinstance(dfc, pd.DataFrame)
    s_c = dfc[dfc["season"] == selected_year].mean(numeric_only=True)

assert isinstance(s_c, pd.Series)
dfca = s_c.to_frame().T.round(1)

layout_columns = st.columns((5.5, 2.5), gap='small')

with layout_columns[1]:
    # plot pie chart
    if st.session_state.selected_division is not None:
        p_chart_name = st.session_state.selected_division
    else:
        p_chart_name = pie_chart_name[language]
    piechart, titlepie = plotly_pie_chart(dfca, p_chart_name, selected_year, language)
    titlepie = f'<p style="font:Courier; color:gray; font-size: 20px;">{titlepie}</p>'
    st.markdown(titlepie, unsafe_allow_html=True)
    st.plotly_chart(piechart, use_container_width=True)

    # plot bar chart
    chart, title = alt_bar_chart(
        df_map,
        selected_indicator,
        indicator_name,
        stat_name,
        col_name,
        selected_season,
        language,
    )
    title = f'<p style="font:Courier; color:gray; font-size: 20px;">{title}</p>'
    st.markdown(title, unsafe_allow_html=True)
    st.altair_chart(chart, use_container_width=True)

with layout_columns[0]:
    left, right = st.columns([0.7, 0.3], gap='small')
    with left:
        st.markdown(f"### {indicator_map[language]}")

    with right:
        st.markdown("<div style='margin-top: 12px;'>", unsafe_allow_html=True)
        if st.session_state.selected_division is not None:
            if st.button(reset_map_label[language]):
                st.session_state.selected_section = None
                reset_map()

    # plot indicators map
    choropleth = make_folium_choropleth(
        geo2plot, selected_indicator, df_map, col_name, language
    )
    map_data = st_folium(choropleth,  height=450, use_container_width=True)

    line_chart, title = make_alt_linechart(
        df_chart,
        selected_indicator,
        indicator_name,
        stat_name,
        unit,
        col_name,
        st.session_state.selected_section,
        language,
    )
    title = f'<p style="font:Courier; color:gray; font-size: 20px;">{title}</p>'
    st.write("")
    st.markdown(title, unsafe_allow_html=True)
    st.altair_chart(line_chart, use_container_width=True)

    if map_data and "last_clicked" in map_data and map_data["last_clicked"] is not None:
        # Find the clicked polygon
        clicked_point = Point(
            map_data["last_clicked"]["lng"], map_data["last_clicked"]["lat"]
        )
        matching_polygon = gdf[gdf.contains(clicked_point)]
        if not matching_polygon.empty:
            clicked_division = matching_polygon.iloc[0]["division"]
            clicked_section = matching_polygon.iloc[0]["section"]
            if (st.session_state.selected_division != clicked_division) or (
                st.session_state.selected_section != clicked_section
            ):
                st.session_state.selected_division = clicked_division
                st.session_state.selected_section = clicked_section
                st.rerun()
