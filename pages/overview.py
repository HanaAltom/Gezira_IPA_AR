import streamlit as st

from util.common2 import logos_and_language
from content.languages import arabic, english
from content.overview_content import arabic_txt, english_txt


language: str = st.session_state.language

with st.sidebar:
    logos_and_language()

if st.session_state.get("language", arabic) == english:
    english_txt()
else:
    arabic_txt()

