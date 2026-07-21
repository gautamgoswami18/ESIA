import streamlit as st

from config import APP_NAME
from config import APP_SUBTITLE

from pathlib import Path


BASE_DIR = Path(__file__).parent

css_file = BASE_DIR / "assets" / "styles.css"

css = css_file.read_text(encoding="utf-8")


st.set_page_config(
    page_title=APP_NAME,
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Custom CSS
st.markdown(
    f"""
    <style>
    {css}
    </style>
    """,
    unsafe_allow_html=True
)

# Home Page

st.title("🤖 ESIRA")

st.caption(APP_SUBTITLE)

st.markdown("---")

st.markdown(
    """
### Welcome to ESIRA 👋

Employee Skill Intelligence & Recruitment Assistant.

From the left menu you can access:

- 📊 Dashboard
- 👥 Employees
- 🤖 ESIRA Assistant

---
"""
)