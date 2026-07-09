import streamlit as st

from services.esira_service import ESIRAService
from renderers.esira_renderer import render
from components.prompt_bar import render_prompt_bar

service = ESIRAService()

st.title("🤖 ESIRA")

st.caption(
    "Employee Skill Intelligence & Recruitment Assistant"
)

prompt = render_prompt_bar()

question = st.text_input(
    "Ask ESIRA",
    value=prompt if prompt else ""
)

search = st.button(
    "🔍 Search",
    use_container_width=True
)

if search and question:

    with st.spinner("ESIRA is searching..."):

        response = service.ask(question)

    render(response)