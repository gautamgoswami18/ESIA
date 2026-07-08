import streamlit as st

from services.dashboard_service import DashboardService
from concurrent.futures import ThreadPoolExecutor

from components.metric_card import render_metric_cards
from components.charts import (
    render_top_skills,
    render_experience
)
from components.tables import (
    render_certifications
)

service = DashboardService()

st.title("📊 Dashboard")

if st.button("🔄 Refresh Dashboard"):
    st.rerun()

with st.spinner("Loading Dashboard..."):

    with ThreadPoolExecutor() as executor:

        summary = executor.submit(service.get_summary)

        skills = executor.submit(service.get_top_skills)

        experience = executor.submit(service.get_experience_distribution)

        certifications = executor.submit(service.get_certifications)

    summary = summary.result()

    skills = skills.result()

    experience = experience.result()

    certifications = certifications.result()

render_metric_cards(summary)

st.divider()

col1, col2 = st.columns([2, 1])

with col1:

    render_top_skills(skills)

with col2:

    render_experience(experience)

st.divider()

render_certifications(certifications)