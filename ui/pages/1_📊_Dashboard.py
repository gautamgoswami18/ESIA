import streamlit as st

from services.dashboard_service import DashboardService

from components.header import render_header
from components.metric_card import render_metric_cards
from components.charts import (
    render_top_skills,
    render_experience
)
from components.tables import render_certifications

service = DashboardService()

render_header()

with st.spinner("Loading Dashboard..."):

    dashboard = service.get_dashboard()

render_metric_cards(
    dashboard["summary"]
)

st.divider()

left, right = st.columns([2,1])

with left:

    render_top_skills(
        dashboard["top_skills"]
    )

with right:

    render_experience(
        dashboard["experience_distribution"]
    )

st.divider()

render_certifications(
    dashboard["certifications"]
)