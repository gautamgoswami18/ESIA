from __future__ import annotations

from html import escape

import streamlit as st

from api_client import APIError
from components.enterprise_ui import (
    configure_page,
    empty_state,
    initials,
    metric_card,
    page_header,
    safe_name,
    status_pill,
)
from services.workforce_service import WorkforceService
from utils.formatter import format_experience_years


configure_page("Employee Directory", "Employees")
service = WorkforceService()

if "employee_page" not in st.session_state:
    st.session_state.employee_page = 1

header_left, header_right = st.columns([5, 1])
with header_left:
    page_header(
        "Employee Directory",
        "PostgreSQL employee records with ChromaDB resume-index status",
    )
with header_right:
    st.write("")
    if st.button(
        "＋ Add Employee",
        type="primary",
        use_container_width=True,
    ):
        st.switch_page("pages/3_AI_Knowledge_Studio.py")

filter_columns = st.columns([2.1, 1.25, 1.25, 1.1, 1.15])
with filter_columns[0]:
    search = st.text_input(
        "Search",
        placeholder="Search employees",
        label_visibility="collapsed",
    )
with filter_columns[1]:
    location = st.text_input(
        "Location",
        placeholder="Location",
        label_visibility="collapsed",
    )
with filter_columns[2]:
    designation = st.text_input(
        "Designation",
        placeholder="Designation",
        label_visibility="collapsed",
    )
with filter_columns[3]:
    status = st.selectbox(
        "Employment status",
        ["All", "active", "inactive", "bench", "notice"],
        label_visibility="collapsed",
    )
with filter_columns[4]:
    page_size = st.selectbox(
        "Rows",
        [10, 20, 50, 100],
        index=0,
        format_func=lambda value: f"{value} / page",
        label_visibility="collapsed",
    )

try:
    payload = service.employees(
        page=st.session_state.employee_page,
        size=page_size,
        search=search,
        location=location,
        designation=designation,
        employment_status=status,
    )
    employees = payload.get("data") or []
    pagination = payload.get("pagination") or {}
except APIError as ex:
    employees = []
    pagination = {}
    st.error(str(ex))

total = pagination.get("total_records") or len(employees)
active = sum(
    str(item.get("employment_status") or "").lower() == "active"
    for item in employees
)
inactive = sum(
    str(item.get("employment_status") or "").lower() == "inactive"
    for item in employees
)
with_resume = 0
indexed = 0
try:
    resume_payload = service.resumes()
    resumes = resume_payload.get("data") or []
    resume_ids = {item.get("employee_id") for item in resumes}
    with_resume = len(resume_ids)
    indexed = sum(bool(item.get("embedding_status")) for item in resumes)
except APIError:
    resumes = []

summary_columns = st.columns(5)
with summary_columns[0]:
    metric_card("Total Employees", f"{total:,}", "👥")
with summary_columns[1]:
    metric_card("Active on Page", active, "✓", tone="green")
with summary_columns[2]:
    metric_card("Inactive on Page", inactive, "◷", tone="amber")
with summary_columns[3]:
    metric_card("Resume Uploaded", with_resume, "▤", tone="purple")
with summary_columns[4]:
    metric_card(
        "Resume Indexed",
        indexed,
        "✦",
        source="ChromaDB AI",
        tone="teal",
    )

with st.container(border=True):
    st.markdown(
        """
        <div class="employee-row header">
          <span>Employee ID</span><span>Employee</span>
          <span>Designation</span><span>Experience</span>
          <span>Location</span><span>Status</span><span>Profile</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not employees:
        empty_state(
            "No employees found",
            "Adjust the filters or add an employee through AI Knowledge Studio.",
            "👥",
        )

    for employee in employees:
        employee_id = employee.get("employee_id")
        name = safe_name(employee)
        designation_text = employee.get("designation") or "Not specified"
        location_text = employee.get("location") or "Not specified"
        years = employee.get("experience_years")
        years_text = format_experience_years(years)
        status_text = employee.get("employment_status") or "Unknown"

        row_columns = st.columns([0.9, 1.5, 1.55, 0.75, 1.1, 0.7, 0.65])
        row_columns[0].markdown(f"`EMP{int(employee_id):04d}`")
        row_columns[1].markdown(
            f"""
            <div class="employee-person">
              <span class="avatar avatar-small">{escape(initials(name))}</span>
              <div><strong>{escape(name)}</strong>
              <small>{escape(employee.get('email') or '')}</small></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        row_columns[2].write(designation_text)
        row_columns[3].write(years_text)
        row_columns[4].write(location_text)
        row_columns[5].markdown(
            status_pill(status_text),
            unsafe_allow_html=True,
        )
        if row_columns[6].button(
            "View",
            key=f"view_employee_{employee_id}",
            use_container_width=True,
        ):
            st.session_state.selected_employee_id = int(employee_id)
            st.switch_page("pages/2_Employee_360.py")

page = int(pagination.get("page") or st.session_state.employee_page)
pages = int(pagination.get("pages") or pagination.get("total_pages") or 1)
previous_col, info_col, next_col = st.columns([1, 4, 1])
with previous_col:
    if st.button(
        "← Previous",
        disabled=page <= 1,
        use_container_width=True,
    ):
        st.session_state.employee_page = page - 1
        st.rerun()
with info_col:
    st.markdown(
        f"<div style='text-align:center;color:#60708e;padding:.55rem'>"
        f"Page {page} of {max(pages, 1)} · {total:,} employees</div>",
        unsafe_allow_html=True,
    )
with next_col:
    if st.button(
        "Next →",
        disabled=page >= pages,
        use_container_width=True,
    ):
        st.session_state.employee_page = page + 1
        st.rerun()
