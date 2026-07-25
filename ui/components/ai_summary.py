import streamlit as st


def render_ai_summary(summary):

    st.subheader("🤖 AI Generated Summary")

    if summary:

        st.info(summary)

    else:

        st.warning(
            "AI summary will appear after resume processing"
        )