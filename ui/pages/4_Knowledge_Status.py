from __future__ import annotations

from html import escape

import streamlit as st

from api_client import APIClient, APIError
from components.enterprise_ui import (
    configure_page,
    empty_state,
    initials,
    metric_card,
    page_header,
    safe_name,
    source_badge,
    status_pill,
)
from services.workforce_service import WorkforceService


configure_page("Resume Knowledge Status", "Knowledge Status")
service = WorkforceService()

header_left, header_actions = st.columns([4.7, 1.8])
with header_left:
    page_header(
        "Resume Knowledge Status",
        "Monitor PostgreSQL resume metadata and ChromaDB indexing",
    )
with header_actions:
    action_columns = st.columns(2)
    with action_columns[0]:
        if st.button(
            "↻ Refresh",
            use_container_width=True,
        ):
            st.rerun()
    with action_columns[1]:
        if st.button(
            "⇧ Upload Resume",
            type="primary",
            use_container_width=True,
        ):
            st.switch_page("pages/3_AI_Knowledge_Studio.py")

try:
    payload = service.resumes()
    resumes = payload.get("data") or []
    load_error = None
except APIError as ex:
    resumes = []
    load_error = str(ex)

indexed = [item for item in resumes if bool(item.get("embedding_status"))]
pending = [item for item in resumes if not bool(item.get("embedding_status"))]
failed = [
    item
    for item in resumes
    if str(item.get("embedding_status") or "").lower() == "failed"
]

metric_columns = st.columns(5)
with metric_columns[0]:
    metric_card("Total Resumes", len(resumes), "▤")
with metric_columns[1]:
    metric_card(
        "Indexed",
        len(indexed),
        "✓",
        source="ChromaDB AI",
        tone="green",
    )
with metric_columns[2]:
    metric_card("Pending", len(pending), "◷", tone="amber")
with metric_columns[3]:
    metric_card("Failed", len(failed), "!", tone="amber")
with metric_columns[4]:
    metric_card(
        "Orphaned Chunks",
        None,
        "◇",
        source="ChromaDB AI",
        tone="purple",
        detail="Requires vector audit API",
    )

with st.container(border=True):
    database_left, database_right = st.columns(2)
    with database_left:
        st.markdown(
            f"""
            <div class="chat-source">
              <strong>{source_badge("PostgreSQL Connected", "postgres")}</strong>
              <p>Employee and resume metadata store operational</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with database_right:
        st.markdown(
            f"""
            <div class="chat-source">
              <strong>{source_badge("ChromaDB Connected", "chroma")}</strong>
              <p>Resume vector-index status is shown per employee</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

if load_error:
    st.error(load_error)


def clear_knowledge_filters() -> None:
    st.session_state.knowledge_search = ""
    st.session_state.knowledge_status_filter = "All"


filter_columns = st.columns([2.1, 1.1, 1.1])
with filter_columns[0]:
    search = st.text_input(
        "Search",
        placeholder="Search by employee or resume file",
        label_visibility="collapsed",
        key="knowledge_search",
    )
with filter_columns[1]:
    status_filter = st.selectbox(
        "Status",
        ["All", "Indexed", "Pending"],
        label_visibility="collapsed",
        key="knowledge_status_filter",
    )
with filter_columns[2]:
    st.button(
        "Clear filters",
        use_container_width=True,
        on_click=clear_knowledge_filters,
    )

filtered = []
for resume in resumes:
    employee_name = safe_name(resume)
    haystack = (
        f"{employee_name} {resume.get('file_name') or ''} "
        f"{resume.get('employee_id') or ''}"
    ).lower()
    if search and search.lower() not in haystack:
        continue
    is_indexed = bool(resume.get("embedding_status"))
    if status_filter == "Indexed" and not is_indexed:
        continue
    if status_filter == "Pending" and is_indexed:
        continue
    filtered.append(resume)

table_column, detail_column = st.columns([3.8, 1.25])
with table_column:
    with st.container(border=True):
        st.markdown(
            """
            <div class="employee-row header" style="
              grid-template-columns:1.45fr 1.6fr 1.1fr 1.05fr .7fr .7fr">
              <span>Employee</span><span>Resume File</span>
              <span>PostgreSQL</span><span>ChromaDB</span>
              <span>Status</span><span>Details</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if not filtered:
            empty_state(
                "No resumes found",
                "Upload and save a resume in AI Knowledge Studio.",
                "▤",
            )
        for resume in filtered:
            employee_id = int(resume.get("employee_id"))
            name = safe_name(resume)
            is_indexed = bool(resume.get("embedding_status"))
            columns = st.columns([1.45, 1.6, 1.1, 1.05, 0.7, 0.7])
            columns[0].markdown(
                f"""
                <div class="employee-person">
                  <span class="avatar avatar-small">{escape(initials(name))}</span>
                  <div><strong>{escape(name)}</strong>
                  <small>EMP{employee_id:04d}</small></div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            columns[1].write(resume.get("file_name") or "—")
            columns[2].markdown(
                status_pill("Stored"),
                unsafe_allow_html=True,
            )
            columns[3].markdown(
                status_pill("Indexed" if is_indexed else "Pending"),
                unsafe_allow_html=True,
            )
            columns[4].markdown(
                status_pill("Success" if is_indexed else "Pending"),
                unsafe_allow_html=True,
            )
            if columns[5].button(
                "View",
                key=f"knowledge_view_{employee_id}",
                use_container_width=True,
            ):
                st.session_state.knowledge_employee_id = employee_id
                st.rerun()

with detail_column:
    selected_id = st.session_state.get("knowledge_employee_id")
    selected = next(
        (
            item
            for item in resumes
            if int(item.get("employee_id")) == int(selected_id)
        ),
        None,
    ) if selected_id else None

    with st.container(border=True):
        if not selected:
            empty_state(
                "Resume details",
                "Select View on a resume to inspect its pipeline state.",
                "◇",
            )
        else:
            selected_name = safe_name(selected)
            employee_id = int(selected["employee_id"])
            is_indexed = bool(selected.get("embedding_status"))
            st.markdown(f"#### {escape(selected_name)}")
            st.markdown(
                status_pill("Success" if is_indexed else "Pending"),
                unsafe_allow_html=True,
            )
            st.markdown("##### Pipeline Steps")
            steps = (
                ("File Uploaded", True),
                ("Metadata Stored (PostgreSQL)", True),
                ("Text Extracted", True),
                ("Embeddings Generated", is_indexed),
                ("Indexed in ChromaDB", is_indexed),
            )
            for label, complete in steps:
                st.markdown(
                    f'<div class="plan-step"><strong>'
                    f'{"✓" if complete else "○"} {escape(label)}</strong>'
                    f'<span>{"Complete" if complete else "Pending"}</span></div>',
                    unsafe_allow_html=True,
                )

            st.markdown("##### File Metadata")
            metadata = (
                ("Employee ID", f"EMP{employee_id:04d}"),
                ("File Name", selected.get("file_name") or "—"),
                (
                    "PostgreSQL",
                    "Stored",
                ),
                (
                    "ChromaDB",
                    "Indexed" if is_indexed else "Pending",
                ),
            )
            for label, value in metadata:
                st.markdown(
                    f'<div class="detail-item"><span>{escape(label)}</span>'
                    f"<span>{escape(str(value))}</span></div>",
                    unsafe_allow_html=True,
                )

            st.markdown("##### Actions")
            st.link_button(
                "⇩ Download Original",
                APIClient.download_url(employee_id),
                use_container_width=True,
            )
            if st.button(
                "↻ Reindex Chroma",
                key=f"reindex_{employee_id}",
                type="primary",
                use_container_width=True,
            ):
                with st.spinner("Generating embeddings and reindexing..."):
                    try:
                        service.reindex(employee_id)
                        st.success("Resume indexed successfully.")
                        st.rerun()
                    except APIError as ex:
                        st.error(str(ex))
            if st.button(
                "Open Employee 360",
                key=f"profile_{employee_id}",
                use_container_width=True,
            ):
                st.session_state.selected_employee_id = employee_id
                st.switch_page("pages/2_Employee_360.py")
