import streamlit as st

from config import APP_NAME
from config import APP_SUBTITLE


st.set_page_config(

    page_title=APP_NAME,

    page_icon="🤖",

    layout="wide",

    initial_sidebar_state="expanded"

)


st.title("🤖 ESIRA")

st.caption(APP_SUBTITLE)

st.markdown("---")

st.markdown(
    """
Welcome to **ESIRA**.

Use the navigation panel on the left to access:

- 📊 Dashboard
- 👥 Employees
- 🤖 ESIRA Assistant
"""
)