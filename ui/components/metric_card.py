import streamlit as st


def metric_card(title, value, icon):

    st.markdown(
        f"""
<div class="metric-card">

<div class="metric-icon">
{icon}
</div>

<div class="metric-title">
{title}
</div>

<div class="metric-value">
{value}
</div>

</div>
""",
        unsafe_allow_html=True
    )


def render_metric_cards(summary):

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        metric_card("Employees", summary["employees"], "👥")

    with col2:
        metric_card("Skills", summary["skills"], "🛠")

    with col3:
        metric_card("Projects", summary["projects"], "📁")

    with col4:
        metric_card("Resumes", summary["resumes"], "📄")

    with col5:
        metric_card("Certificates", summary["certifications"], "🏆")