import streamlit as st

from util import common2 as cm
from util.gezira_info_txt import arabic_txt, english_txt


cm.set_page_container_style(
    max_width=1100,
    max_width_100_percent=True,
    padding_top=0,
    padding_right=0,
    padding_left=0,
    padding_bottom=0,
)

logo_small, logo_wide = cm.logos()

with st.sidebar:
    st.logo(
        logo_wide, size="large", link="https://www.un-ihe.org/", icon_image=logo_small
    )
    if st.button("العربية"):
        st.session_state.language = "a"
    if st.button("English"):
        st.session_state.language = "e"

if st.session_state.get("language", "a") == "e":
    english_txt()
else:
    arabic_txt()
