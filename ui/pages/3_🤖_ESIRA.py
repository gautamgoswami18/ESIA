import streamlit as st

from services.esira_service import ESIRAService
from renderers.esira_renderer import render
from components.prompt_bar import render_prompt_bar

service = ESIRAService()

st.title("🤖 ESIRA")
st.caption("Employee Skill Intelligence & Recruitment Assistant")

# -----------------------------
# Session State
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# Chat History
# -----------------------------
chat_container = st.container()

with chat_container:

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            if message["role"] == "assistant":
                render(message["content"])
            else:
                st.markdown(message["content"])


# -----------------------------
# Suggested Prompts
# -----------------------------
prompt = render_prompt_bar()


# -----------------------------
# Chat Input
# -----------------------------
question = st.chat_input(
    "Ask ESIRA..."
)

if not question and prompt:
    question = prompt

if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):

        with st.spinner("🤖 ESIRA is thinking..."):

            response = service.ask(question)

            render(response)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )

    st.rerun()