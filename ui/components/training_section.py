import streamlit as st


def render_training(training):

    st.subheader("📚 Training")

    container = st.container(border=True)

    with container:

        if not training:
            st.info("No training extracted.")
            return

        for item in training:

            if isinstance(item, dict):
                name = item.get("name") or "-"
                technology = item.get("technology") or "-"
                provider = item.get("provider") or "-"
                score = item.get("score") or "-"
            else:
                name = getattr(item, "name", "-")
                technology = getattr(item, "technology", None) or "-"
                provider = getattr(item, "provider", None) or "-"
                score = getattr(item, "score", None) or "-"

            with st.container(border=True):
                st.markdown(f"### {name}")
                col1, col2, col3 = st.columns(3)
                col1.write(f"**Technology:** {technology}")
                col2.write(f"**Provider:** {provider}")
                col3.write(f"**Score:** {score}")

    st.divider()
