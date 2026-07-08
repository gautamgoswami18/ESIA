import streamlit as st


def render_metric_cards(summary):

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            label="👥 Employees",
            value=summary["employees"]
        )

    with col2:
        st.metric(
            label="🛠 Skills",
            value=summary["skills"]
        )

    with col3:
        st.metric(
            label="📁 Projects",
            value=summary["projects"]
        )

    with col4:
        st.metric(
            label="📄 Resumes",
            value=summary["resumes"]
        )

    with col5:
        st.metric(
            label="🏆 Certifications",
            value=summary["certifications"]
        )