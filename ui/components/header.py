import streamlit as st


def render_header():

    col1, col2 = st.columns([8, 1])

    with col1:

        st.title("📊 ESIRA Dashboard")

        st.caption(
            "Employee Skill Intelligence & Recruitment Assistant"
        )

    with col2:

        if st.button("🔄 Refresh"):

            st.rerun()