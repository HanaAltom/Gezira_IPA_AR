from os.path import join

import streamlit as st
from arabic_support import support_arabic_text
import altair as alt

from content.languages import arabic, english


# Page configuration
st.set_page_config(
    page_title="Gezira Irrigation Scheme Irrigation Performance Indicators by Sections Dashboard",
    page_icon="📈🌿",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

st.markdown("""
    <style>
    header.stAppHeader {
        background-color: transparent;
    }
    section.stMain .block-container {
        padding-top: 0rem;
        z-index: 1;
    }
    </style>""", unsafe_allow_html=True)

hide_github_icon = """
    <style>
        .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob, .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137, .viewerBadge_text__1JaDK{ display: none; } #MainMenu{ visibility: hidden; } footer { visibility: hidden; } header { visibility: hidden; }
    </style>
"""
st.markdown(hide_github_icon, unsafe_allow_html=True)


# setup pages
if "language" not in st.session_state or st.session_state.language == arabic:
    st.session_state["language"] = arabic
    support_arabic_text(all=True)
    language = arabic
    overview_page_name = "ملخّص"
    ipa_page_name = "مؤشّرات أداء الري"
    raster_viewer_page_name = "عارض الخرائط"
elif st.session_state.language == english:
    st.session_state["language"] = english
    support_arabic_text(all=False)
    language = english
    overview_page_name = "Overview"
    ipa_page_name = "Irrigation Performance Indicators"
    raster_viewer_page_name = "Raster Viewer"
else:
    raise NotImplementedError("language not supported")

overview_page = st.Page(join("pages", "overview.py"), title=overview_page_name)
ipa_page = st.Page(join("pages", "ipa.py"), title=ipa_page_name)
raster_viewer_page = st.Page(join("pages", "raster_viewer.py"), title=raster_viewer_page_name)
pg = st.navigation([overview_page, ipa_page, raster_viewer_page])
pg.run()
