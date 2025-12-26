import streamlit as st
from st_pages import get_nav_from_toml

st.set_page_config(page_title="Toy Arcade", layout="centered")

nav = get_nav_from_toml(".streamlit/pages.toml")
st.navigation(nav).run()