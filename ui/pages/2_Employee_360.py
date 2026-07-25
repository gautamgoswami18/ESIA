from __future__ import annotations

from html import escape

import streamlit as st

from api_client import APIClient, APIError
from components.enterprise_ui import (
    chips,
    configure_page,
    empty_state,
    initials,
    page_header,
    safe_name,
    source_badge,
    status_pill,
)
from services.workforce_service import WorkforceService


configure_page("Employee 360", "Employee 360")
service = WorkforceService()


def choose_employee() -> int | None:
    selected = st.session_state.get("selected_employee_id")
    query_value = st.query_params.get("employee_id")
    if query_value:
        try:
            selected = int(query_value)
        except (TypeError, ValueError):
            pass
    if selected:
        return int(selected)

    try:
        payload = service.employees(page=1, size=100)
        options = payload.get("data") or []
    except APIError:
        options = []
    if not options:
        return None
    labels = {
        int(item["employee_id"]): (
            f"EMP{int(item['employee_id']):04d} · {safe_name(item)}"
        )
        for item in options
    }
    return st.selectbox(
        "Select an employee",
        list(labels),
        format_func=lambda value: labels[value],
    )


employee_id = choose_employee()
if employee_id is None:
    page_header(
        "Employee 360",
        "Select an employee from the directory to view their profile.",
    )
    empty_state(
        "No employee selected",
        "Open Employee Directory and choose View Profile.",
        "👤",
    )
    if st.button("Open Employee Directory", type="primary"):
        st.switch_page("pages/1_Employees.py")
    st.stop()

st.session_state.selected_employee_id = employee_id

try:
    employee_payload = service.employee(employee_id)
    employee = employee_payload.get("data") or {}
except APIError as ex:
    st.error(str(ex))
    st.stop()

profile_error = None
try:
    profile_payload = service.employee_profile(employee_id)
    profile = profile_payload.get("data") or {}
except APIError as ex:
    profile = {}
    profile_error = str(ex)

resume = profile.get("resume") or {}
try:
    resume_payload = service.resume(employee_id)
    resume = {**resume, **(resume_payload.get("data") or {})}
except APIError:
    pass

name = safe_name(employee)
header_left, header_actions = st.columns([4.5, 2])
with header_left:
    page_header(
        f"Employees / EMP{employee_id:04d}",
        "PostgreSQL employee record joined with resume intelligence",
    )
with header_actions:
    action_columns = st.columns(2)
    with action_columns[0]:
        st.link_button(
            "⇩ Download Resume",
            APIClient.download_url(employee_id),
            type="primary",
            use_container_width=True,
            disabled=not bool(resume),
        )
    with action_columns[1]:
        if st.button("← Directory", use_container_width=True):
            st.switch_page("pages/1_Employees.py")

with st.container(border=True):
    status = employee.get("employment_status") or "Unknown"
    resume_status = (
        "Resume Indexed"
        if resume.get("embedding_status")
        else ("Resume Uploaded" if resume else "No Resume")
    )
    st.markdown(
        f"""
        <div class="profile-hero">
          <span class="avatar avatar-large">{escape(initials(name))}</span>
          <div>
            <h2>{escape(name)}</h2>
            <p>{escape(employee.get('designation') or 'Designation not set')}</p>
            <div class="profile-meta">
              <span>⌖ {escape(employee.get('location') or 'Location not set')}</span>
              <span>▣ {escape(str(employee.get('experience_years') or 0))} years</span>
              {status_pill(status)}
              {status_pill(resume_status)}
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

record_column, intelligence_column = st.columns([1.05, 2.65])

with record_column:
    with st.container(border=True):
        st.markdown(
            f'<div class="section-title"><span>Employee Record</span>'
            f'{source_badge("PostgreSQL", "postgres")}</div>',
            unsafe_allow_html=True,
        )
        details = (
            ("Employee ID", f"EMP{employee_id:04d}"),
            ("Email", employee.get("email") or "—"),
            ("Location", employee.get("location") or "—"),
            ("Designation", employee.get("designation") or "—"),
            (
                "Experience",
                f"{employee.get('experience_years') or 0} years",
            ),
            (
                "Joining Date",
                employee.get("joining_date") or "Not recorded",
            ),
            (
                "Resume File",
                resume.get("file_name") or "Not uploaded",
            ),
            ("Status", employee.get("employment_status") or "—"),
        )
        detail_html = "".join(
            f'<div class="detail-item"><span>{escape(label)}</span>'
            f"<span>{escape(str(value))}</span></div>"
            for label, value in details
        )
        st.markdown(
            f'<div class="detail-list">{detail_html}</div>',
            unsafe_allow_html=True,
        )

with intelligence_column:
    with st.container(border=True):
        st.markdown(
            f'<div class="section-title"><span>AI Resume Intelligence</span>'
            f'{source_badge("ChromaDB AI", "chroma")}</div>',
            unsafe_allow_html=True,
        )

        if profile_error:
            st.warning(
                "The employee record loaded, but structured resume "
                "intelligence is not currently available from the backend."
            )

        summary = profile.get("summary")
        if summary:
            st.markdown("**Executive Summary**")
            st.write(summary)
        else:
            st.caption(
                "No AI summary is available. Index a resume in AI Knowledge "
                "Studio, then use ESIRA Assistant for semantic retrieval."
            )

        skills = profile.get("skills") or []
        st.markdown("**Skills**")
        if skills:
            st.markdown(chips(skills), unsafe_allow_html=True)
        else:
            empty_state(
                "No skills returned",
                "Skills are kept in ChromaDB, not in esia.skills.",
                "✦",
            )

        projects = profile.get("projects") or []
        st.markdown("**Projects**")
        if projects:
            for project in projects:
                project_name = (
                    project.get("name")
                    or project.get("project_name")
                    or "Untitled project"
                )
                technologies = project.get("technologies") or []
                st.markdown(
                    f"""
                    <div class="project-card">
                      <strong>{escape(project_name)}</strong>
                      <div class="project-meta">
                        {escape(project.get('client') or 'Client not stated')}
                        · {escape(project.get('role') or 'Role not stated')}
                      </div>
                      <p>{escape(project.get('description') or '')}</p>
                      {chips(technologies)}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.caption("No projects were returned from resume intelligence.")

        training = profile.get("training") or []
        st.markdown("**Training**")
        if training:
            training_rows = []
            for item in training:
                training_rows.append(
                    {
                        "Training": item.get("name") or "—",
                        "Technology": item.get("technology") or "—",
                        "Provider": item.get("provider") or "—",
                        "Score": item.get("score") or "—",
                    }
                )
            st.dataframe(
                training_rows,
                hide_index=True,
                use_container_width=True,
            )
        else:
            st.caption("No training was found in this resume.")

        certifications = profile.get("certifications") or []
        st.markdown("**Certifications**")
        if certifications:
            certification_rows = []
            for item in certifications:
                certification_rows.append(
                    {
                        "Certification": (
                            item.get("name")
                            or item.get("certification_name")
                            or "—"
                        ),
                        "Issuer": (
                            item.get("issuing_organization")
                            or item.get("vendor")
                            or "—"
                        ),
                        "Issued": item.get("issue_date") or "—",
                        "Expires": item.get("expiry_date") or "—",
                    }
                )
            st.dataframe(
                certification_rows,
                hide_index=True,
                use_container_width=True,
            )
        else:
            st.info("No certifications were found in this resume.")
