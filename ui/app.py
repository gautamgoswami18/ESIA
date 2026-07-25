from __future__ import annotations

from collections import Counter

import pandas as pd
import streamlit as st

from api_client import APIError
from components.enterprise_ui import (
    configure_page,
    empty_state,
    metric_card,
    page_header,
    source_badge,
)
from services.workforce_service import WorkforceService


configure_page("Workforce Overview", "Overview")
service = WorkforceService()


def load_workforce():
    errors = []
    employees_payload = {}
    active_payload = {}
    resumes_payload = {}
    try:
        employees_payload = service.employees(page=1, size=100)
        active_payload = service.employees(
            page=1,
            size=1,
            employment_status="active",
        )
    except APIError as ex:
        errors.append(str(ex))
    try:
        resumes_payload = service.resumes()
    except APIError as ex:
        errors.append(str(ex))
    return (
        employees_payload,
        active_payload,
        resumes_payload,
        errors,
    )


(
    employees_payload,
    active_payload,
    resumes_payload,
    errors,
) = load_workforce()
employees = employees_payload.get("data") or []
pagination = employees_payload.get("pagination") or {}
resumes = resumes_payload.get("data") or []

page_header(
    "Workforce Overview",
    "Unified view of employee metadata and AI-powered resume intelligence",
)

if errors:
    st.warning(
        "Some live data could not be loaded. "
        "Start the FastAPI backend to populate all dashboard sections."
    )

total_employees = pagination.get("total_records") or len(employees)
active_employees = (
    (active_payload.get("pagination") or {}).get("total_records")
    if active_payload
    else None
)
inactive_employees = sum(
    str(employee.get("employment_status") or "").lower() == "inactive"
    for employee in employees
)
indexed_resumes = sum(
    1 for resume in resumes if bool(resume.get("embedding_status"))
)

metric_columns = st.columns(6)
with metric_columns[0]:
    metric_card("Total Employees", f"{total_employees:,}", "👥")
with metric_columns[1]:
    metric_card(
        "Active Employees",
        f"{active_employees:,}" if active_employees is not None else None,
        "✓",
        tone="green",
    )
with metric_columns[2]:
    metric_card(
        "Inactive Employees",
        f"{inactive_employees:,}",
        "◷",
        tone="amber",
    )
with metric_columns[3]:
    metric_card("Resumes Indexed", f"{indexed_resumes:,}", "▤", tone="purple")
with metric_columns[4]:
    metric_card(
        "AI Skills Discovered",
        None,
        "✦",
        source="ChromaDB AI",
        tone="teal",
        detail="Query through ESIRA",
    )
with metric_columns[5]:
    metric_card(
        "Certifications Found",
        None,
        "◇",
        source="ChromaDB AI",
        tone="teal",
        detail="Query through ESIRA",
    )

st.markdown(
    f"""
    <div style="margin:.8rem 0 1rem;color:#61708a;font-size:.72rem">
      {source_badge("PostgreSQL", "postgres")}
      &nbsp; Authoritative employee and resume metadata
      &nbsp;&nbsp;&nbsp;
      {source_badge("AI Extracted", "chroma")}
      &nbsp; ChromaDB resume intelligence
    </div>
    """,
    unsafe_allow_html=True,
)

chart_left, chart_middle, chart_right = st.columns([1, 1, 1.3])
with chart_left:
    with st.container(border=True):
        st.markdown("#### Experience Distribution")
        experience_counts = Counter()
        for employee in employees:
            years = float(employee.get("experience_years") or 0)
            if years < 2:
                band = "0–2 years"
            elif years < 5:
                band = "2–5 years"
            elif years < 10:
                band = "5–10 years"
            elif years < 15:
                band = "10–15 years"
            else:
                band = "15+ years"
            experience_counts[band] += 1
        if experience_counts:
            frame = pd.DataFrame(
                {
                    "Experience": list(experience_counts),
                    "Employees": list(experience_counts.values()),
                }
            ).set_index("Experience")
            st.bar_chart(frame, color="#0b5de8", height=270)
        else:
            empty_state(
                "No employee data",
                "Experience distribution appears when employee records load.",
            )

with chart_middle:
    with st.container(border=True):
        st.markdown("#### Employees by Location")
        locations = Counter(
            employee.get("location") or "Not specified"
            for employee in employees
        )
        if locations:
            frame = pd.DataFrame(
                {
                    "Location": list(locations),
                    "Employees": list(locations.values()),
                }
            ).set_index("Location")
            st.bar_chart(
                frame.sort_values("Employees", ascending=False).head(8),
                color="#079c97",
                horizontal=True,
                height=270,
            )
        else:
            empty_state(
                "No location data",
                "Location analytics appears when employee records load.",
            )

with chart_right:
    with st.container(border=True):
        st.markdown("#### Top AI-Extracted Skills")
        empty_state(
            "Semantic skill analytics",
            "Skills live only in ChromaDB. Use ESIRA Assistant to search "
            "and compare them without duplicating skill records in PostgreSQL.",
            "✦",
        )
        if st.button(
            "Open ESIRA Assistant",
            key="overview_open_esira",
            use_container_width=True,
        ):
            st.switch_page("pages/5_ESIRA_Assistant.py")

with st.container(border=True):
    title_col, action_col = st.columns([5, 1])
    with title_col:
        st.markdown("#### Recent Resume Activity")
    with action_col:
        if st.button(
            "View knowledge status",
            key="overview_status",
            use_container_width=True,
        ):
            st.switch_page("pages/4_Knowledge_Status.py")

    if resumes:
        activity = []
        for resume in resumes[:8]:
            name = " ".join(
                part
                for part in (
                    resume.get("first_name"),
                    resume.get("last_name"),
                )
                if part
            )
            activity.append(
                {
                    "Employee ID": resume.get("employee_id"),
                    "Employee": name or "—",
                    "Resume File": resume.get("file_name") or "—",
                    "PostgreSQL Metadata": "Stored",
                    "ChromaDB Index": (
                        "Indexed"
                        if resume.get("embedding_status")
                        else "Pending"
                    ),
                }
            )
        st.dataframe(
            activity,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Employee ID": st.column_config.NumberColumn(format="%d"),
            },
        )
    else:
        empty_state(
            "No resume activity",
            "Processed and saved resumes will appear here.",
            "▤",
        )
