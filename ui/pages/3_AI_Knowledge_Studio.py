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
    source_badge,
)
from services.workforce_service import WorkforceService


configure_page("AI Knowledge Studio", "AI Knowledge Studio")
client = APIClient()
service = WorkforceService()

STATE_DEFAULTS = {
    "studio_profile": None,
    "studio_process_id": None,
    "studio_match": None,
    "studio_saved": False,
    "studio_employee_id": None,
    "studio_file_name": None,
}
for key, value in STATE_DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


def clear_studio() -> None:
    for key, value in STATE_DEFAULTS.items():
        st.session_state[key] = value


def pipeline_html(processed: bool, saved: bool) -> str:
    steps = (
        ("Resume Uploaded", processed),
        ("PDF Parsed", processed),
        ("Employee Identified", processed),
        ("Skills Extracted", processed),
        ("Projects Extracted", processed),
        ("Training Extracted", processed),
        ("Profile Preview", processed),
        ("Vector Embeddings", saved),
        ("Knowledge Base", saved),
    )
    cards = []
    for index, (label, complete) in enumerate(steps, start=1):
        state = "completed" if complete else "pending"
        note = ""
        if not complete and index >= 8:
            note = '<div class="step-note">Runs after Save</div>'
        node = "✓" if complete else str(index)
        cards.append(
            f'<div class="pipeline-step {state}">'
            f'<span class="step-node">{node}</span>'
            f'<div class="step-label">{escape(label)}</div>{note}</div>'
        )
    return f'<div class="pipeline">{"".join(cards)}</div>'


page_header(
    "AI Knowledge Studio",
    "Upload, review, and save resume intelligence",
)

with st.container(border=True):
    st.markdown("#### Upload Resume")
    st.markdown(
        """
        <div class="resume-drop">
          <span class="resume-drop-icon">⇧</span>
          <div><strong>Drag and drop a PDF file below</strong>
          <small>PDF only · Maximum file size 10 MB · Processing creates a preview</small></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    uploaded_file = st.file_uploader(
        "Resume PDF",
        type=["pdf"],
        label_visibility="collapsed",
        key="studio_uploader",
    )
    upload_left, upload_right = st.columns([5, 1])
    with upload_left:
        if uploaded_file:
            st.caption(
                f"Selected: {uploaded_file.name} · "
                f"{len(uploaded_file.getvalue()) / 1024:.1f} KB"
            )
    with upload_right:
        process_clicked = st.button(
            "Process Resume",
            type="primary",
            disabled=uploaded_file is None,
            use_container_width=True,
        )

if process_clicked:
    if uploaded_file.size > 10 * 1024 * 1024:
        st.error("The selected PDF exceeds the 10 MB limit.")
    else:
        with st.spinner("Extracting text and building the AI profile..."):
            try:
                response = client.process_resume(uploaded_file)
                data = response.get("data") or {}
                st.session_state.studio_profile = (
                    data.get("employee_profile") or {}
                )
                st.session_state.studio_process_id = data.get("process_id")
                st.session_state.studio_match = {
                    "matched": bool(data.get("matched")),
                    "confidence": data.get("confidence"),
                    "action": data.get("action"),
                }
                st.session_state.studio_saved = False
                st.session_state.studio_employee_id = None
                st.session_state.studio_file_name = uploaded_file.name
                st.rerun()
            except APIError as ex:
                st.error(f"Unable to process resume: {ex}")

processed = bool(st.session_state.studio_profile)
saved = bool(st.session_state.studio_saved)

with st.container(border=True):
    st.markdown(pipeline_html(processed, saved), unsafe_allow_html=True)

profile = st.session_state.studio_profile or {}
match = st.session_state.studio_match or {}

if match:
    if match.get("matched"):
        st.success(
            "Existing employee identified "
            f"({match.get('confidence') or 0}% confidence). "
            "Save will update employee metadata and replace the ChromaDB index."
        )
    else:
        st.info(
            "New employee profile. Save will create the employee and resume "
            "metadata in PostgreSQL, then index resume intelligence in ChromaDB."
        )

if profile:
    with st.container(border=True):
        st.markdown("#### Profile Preview")
        identity_column, intelligence_column, learning_column = st.columns(
            [1.05, 1.7, 1.45]
        )

        with identity_column:
            full_name = (
                f"{profile.get('first_name') or ''} "
                f"{profile.get('last_name') or ''}"
            ).strip() or "Unnamed employee"
            st.markdown(
                f"""
                <div class="profile-hero">
                  <span class="avatar">{escape(initials(full_name))}</span>
                  <div><h2 style="font-size:1.25rem">{escape(full_name)}</h2>
                  <p>{escape(profile.get('designation') or '—')}</p></div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            details = (
                ("Email", profile.get("email") or "—"),
                ("Phone", profile.get("phone") or "—"),
                ("Experience", f"{profile.get('experience_years') or 0} years"),
                ("Location", profile.get("location") or "—"),
                ("Department", profile.get("department") or "—"),
            )
            st.markdown(
                '<div class="detail-list">'
                + "".join(
                    f'<div class="detail-item"><span>{escape(label)}</span>'
                    f"<span>{escape(str(value))}</span></div>"
                    for label, value in details
                )
                + "</div>",
                unsafe_allow_html=True,
            )

        with intelligence_column:
            skills = profile.get("skills") or []
            st.markdown(f"**Skills ({len(skills)})**")
            if skills:
                st.markdown(chips(skills), unsafe_allow_html=True)
            else:
                st.caption("No skills extracted.")

            projects = profile.get("projects") or []
            st.markdown(f"**Projects ({len(projects)})**")
            if projects:
                for project in projects:
                    name = (
                        project.get("name")
                        or project.get("project_name")
                        or "Untitled project"
                    )
                    st.markdown(
                        f"""
                        <div class="project-card">
                          <strong>{escape(name)}</strong>
                          <div class="project-meta">
                            {escape(project.get('client') or 'Client not stated')}
                            · {escape(project.get('role') or 'Role not stated')}
                          </div>
                          <p>{escape(project.get('description') or '')}</p>
                          {chips(project.get('technologies') or [])}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
            else:
                st.caption("No projects extracted.")

        with learning_column:
            training = profile.get("training") or []
            st.markdown(f"**Training ({len(training)})**")
            if training:
                st.dataframe(
                    [
                        {
                            "Training": item.get("name") or "—",
                            "Provider": item.get("provider") or "—",
                            "Technology": item.get("technology") or "—",
                        }
                        for item in training
                    ],
                    hide_index=True,
                    use_container_width=True,
                )
            else:
                st.caption("No training extracted.")

            certifications = profile.get("certifications") or []
            st.markdown(f"**Certifications ({len(certifications)})**")
            if certifications:
                st.dataframe(
                    [
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
                        }
                        for item in certifications
                    ],
                    hide_index=True,
                    use_container_width=True,
                )
            else:
                empty_state(
                    "No certifications found",
                    "This is a valid result when the resume contains none.",
                    "◇",
                )

        if profile.get("summary"):
            st.markdown("**AI Summary**")
            st.write(profile["summary"])

if saved:
    st.success(
        "Save completed. Employee and resume metadata are in PostgreSQL; "
        "skills, projects, training, certifications, summary, and resume "
        "content are searchable through ChromaDB."
    )

if profile:
    with st.container(border=True):
        action_info, clear_column, save_column = st.columns([5, 1, 1.35])
        with action_info:
            st.markdown(
                f"""
                <div class="info-strip">
                  <span>ⓘ</span><span>Save writes employee + resume metadata to
                  {source_badge("PostgreSQL", "postgres")} and indexes extracted
                  resume intelligence in {source_badge("ChromaDB", "chroma")}.
                  No skill master row is created.</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with clear_column:
            if st.button("Clear", use_container_width=True):
                clear_studio()
                st.rerun()
        with save_column:
            save_clicked = st.button(
                "▣ Save Employee",
                type="primary",
                disabled=saved,
                use_container_width=True,
            )

    if save_clicked:
        with st.spinner("Saving metadata and indexing ChromaDB..."):
            try:
                response = service.save_resume(
                    st.session_state.studio_process_id
                )
                data = response.get("data") or {}
                st.session_state.studio_saved = True
                st.session_state.studio_employee_id = data.get("employee_id")
                if data.get("employee_id"):
                    st.session_state.selected_employee_id = int(
                        data["employee_id"]
                    )
                st.rerun()
            except APIError as ex:
                st.error(f"Unable to save the processed resume: {ex}")
else:
    empty_state(
        "Resume preview will appear here",
        "Select a PDF and click Process Resume. Nothing is persisted until Save.",
        "▤",
    )
