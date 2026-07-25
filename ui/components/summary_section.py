import streamlit as st


def render_summary(summary: str):

    st.subheader("🤖 AI Summary")

    container = st.container(border=True)

    with container:

        if not summary:

            st.info(
                "AI summary will appear here after processing the resume."
            )

            st.divider()

            return

        st.markdown(summary)

    st.divider() 