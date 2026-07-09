import streamlit as st

PROMPTS = [
    "Find Java Developers",
    "Find Python Developers",
    "Compare Employee 1001 and 1002",
    "Summarize Employee 1005",
    "Find AI Engineers",
    "Find React Developers"
]


def render_prompt_bar():

    st.markdown("### 💡 Suggested Prompts")

    cols = st.columns(3)

    selected = None

    for index, prompt in enumerate(PROMPTS):

        if cols[index % 3].button(
            prompt,
            use_container_width=True
        ):
            selected = prompt

    return selected