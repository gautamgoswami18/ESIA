import streamlit as st


PROMPTS = [
    "👨‍💻 Find Java Developers",
    "🐍 Find Python Developers",
    "🤖 Find AI Engineers",
    "⚖️ Compare Employee 1001 & 1002",
    "📄 Summary of Employee 1098",
]


def render_prompt_bar():

    st.markdown(
        """
        <div class="prompt-container">
        </div>
        """,
        unsafe_allow_html=True,
    )

    cols = st.columns(len(PROMPTS))

    selected_prompt = None

    for col, prompt in zip(cols, PROMPTS):

        with col:

            if st.button(
                prompt,
                key=f"prompt_{prompt}",
                use_container_width=True,
            ):
                selected_prompt = prompt

    return selected_prompt