from __future__ import annotations

from html import escape
import re
from typing import Any

import streamlit as st

from api_client import APIError
from components.enterprise_ui import (
    chips,
    configure_page,
    empty_state,
    initials,
    page_header,
    safe_name,
    source_badge,
)
from services.workforce_service import WorkforceService


configure_page("ESIRA Assistant", "ESIRA Assistant")
service = WorkforceService()

if "esira_messages" not in st.session_state:
    st.session_state.esira_messages = []
if "esira_conversations" not in st.session_state:
    st.session_state.esira_conversations = []


@st.cache_data(ttl=120, show_spinner=False)
def load_summary_profile(employee_id: int) -> dict:
    payload = WorkforceService().employee_profile(employee_id)
    return payload.get("data") or {}


def summary_employee_id(
    response: dict[str, Any],
    message_index: int,
) -> int | None:
    value = response.get("employee_id")
    if value is not None:
        try:
            return int(value)
        except (TypeError, ValueError):
            pass

    if message_index <= 0:
        return None

    messages = st.session_state.get("esira_messages") or []
    if message_index > len(messages) - 1:
        return None

    previous = messages[message_index - 1]
    if previous.get("role") != "user":
        return None

    match = re.search(
        r"\bEMP(?:LOYEE)?\s*[-:#]?\s*(\d+)\b",
        str(previous.get("content") or ""),
        flags=re.IGNORECASE,
    )
    return int(match.group(1)) if match else None


def format_summary_experience(value: Any) -> str | None:
    if value in (None, ""):
        return None
    try:
        years = float(value)
    except (TypeError, ValueError):
        return None
    formatted = f"{years:.1f}".rstrip("0").rstrip(".")
    return f"{formatted} years"


def render_employee_summary(
    response: dict[str, Any],
    summary: str,
    message_index: int,
) -> bool:
    employee_id = summary_employee_id(response, message_index)
    if employee_id is None:
        return False

    profile = {}
    profile_error = None
    try:
        profile = load_summary_profile(employee_id)
    except APIError as ex:
        profile_error = str(ex)

    employee = profile.get("employee") or {}
    name = (
        safe_name(employee)
        if employee
        else f"Employee EMP{employee_id:04d}"
    )
    designation = employee.get("designation") or "Role not specified"
    experience = format_summary_experience(
        employee.get("experience_years")
    )
    location = employee.get("location")
    status = employee.get("employment_status")
    skills = profile.get("skills") or []
    projects = profile.get("projects") or []
    training = profile.get("training") or []
    certifications = profile.get("certifications") or []
    primary_skill = profile.get("primary_skill")

    metadata = [
        value
        for value in (experience, location, status)
        if value
    ]
    metadata_html = "".join(
        f'<span class="summary-meta-pill">{escape(str(value))}</span>'
        for value in metadata
    )
    safe_summary = escape(summary).replace("\n", "<br>")
    skills_html = chips(skills, limit=10)
    if primary_skill:
        skills_html = (
            f'<span class="chip primary">'
            f"{escape(str(primary_skill))}</span>"
            f"{skills_html}"
        )
    remaining_skills = max(len(skills) - 10, 0)
    if remaining_skills:
        skills_html += (
            f'<span class="summary-more-chip">+{remaining_skills} more</span>'
        )

    skills_section_html = (
        (
            '<div class="summary-section-label summary-skills-label">'
            "Core skills"
            "</div>"
            f'<div class="summary-skills">{skills_html}</div>'
        )
        if skills_html
        else ""
    )
    has_structured_details = bool(
        primary_skill
        or skills
        or projects
        or training
        or certifications
    )
    profile_details_html = (
        (
            '<div class="summary-stat-grid">'
            '<div class="summary-stat">'
            f"<strong>{len(skills)}</strong><span>Skills</span>"
            "</div>"
            '<div class="summary-stat">'
            f"<strong>{len(projects)}</strong><span>Projects</span>"
            "</div>"
            '<div class="summary-stat">'
            f"<strong>{len(training)}</strong><span>Training</span>"
            "</div>"
            '<div class="summary-stat">'
            f"<strong>{len(certifications)}</strong>"
            "<span>Certifications</span>"
            "</div>"
            "</div>"
        )
        if has_structured_details
        else ""
    )

    st.html(
        f"""
        <div class="assistant-summary-card">
          <div class="assistant-summary-hero">
            <span class="summary-avatar">{escape(initials(name))}</span>
            <div class="summary-identity">
              <div class="summary-eyebrow">Employee intelligence</div>
              <h3>{escape(name)}</h3>
              <p>{escape(str(designation))}</p>
              <div class="summary-meta">
                <span class="summary-id">EMP{employee_id:04d}</span>
                {metadata_html}
              </div>
            </div>
            <span class="summary-ai-label">AI Resume Summary</span>
          </div>
          <div class="assistant-summary-body">
            <div class="summary-section-label">Executive summary</div>
            <div class="summary-copy">{safe_summary}</div>
            {skills_section_html}
            {profile_details_html}
          </div>
          <div class="assistant-summary-footer">
            <span class="summary-source-dot"></span>
            Resume intelligence from ChromaDB, identity verified in PostgreSQL
          </div>
        </div>
        """
    )

    footer_left, footer_action = st.columns([3.3, 1.2])
    with footer_left:
        if profile_error:
            st.caption(
                "The summary is available, but structured profile details "
                f"could not be loaded: {profile_error}"
            )
        else:
            st.caption(
                "AI-generated summary. Verify important staffing decisions "
                "against the employee profile and original resume."
            )
    with footer_action:
        if st.button(
            "View Employee 360",
            icon=":material/person:",
            key=f"summary_profile_{message_index}_{employee_id}",
            width="stretch",
        ):
            st.session_state.selected_employee_id = employee_id
            st.switch_page("pages/2_Employee_360.py")

    return True


def candidate_score(candidate: dict) -> float | None:
    for key in ("match_score", "score", "similarity"):
        value = candidate.get(key)
        if value is None or isinstance(value, bool):
            continue
        try:
            score = float(value)
        except (TypeError, ValueError):
            continue
        if 0 <= score <= 100:
            return score
    return None


def candidate_rank(candidate: dict) -> int:
    try:
        return int(candidate.get("rank"))
    except (TypeError, ValueError):
        return 999


def ranked_candidates(answer: dict[str, Any]) -> list[dict]:
    best = answer.get("best_candidate")
    others = answer.get("other_candidates") or []
    candidates = (
        ([best] if isinstance(best, dict) else [])
        + [
            candidate
            for candidate in others
            if isinstance(candidate, dict)
        ]
    )
    return sorted(
        candidates,
        key=lambda candidate: (
            candidate_score(candidate) is None,
            -(candidate_score(candidate) or 0),
            candidate_rank(candidate),
        ),
    )


def render_candidate(
    candidate: dict,
    rank: int,
    widget_scope: str,
) -> None:
    employee_id = candidate.get("employee_id")
    name = (
        candidate.get("name")
        or candidate.get("employee_name")
        or (
            f"Employee {employee_id}"
            if employee_id
            else "Employee identity unavailable"
        )
    )
    skills_value = (
        candidate.get("matched_requirements")
        or candidate.get("matching_skills")
        or candidate.get("skills")
        or []
    )
    missing_requirements = candidate.get("missing_requirements") or []
    requirement_evidence = candidate.get("requirement_evidence") or []
    score_breakdown = candidate.get("score_breakdown") or {}
    score = candidate_score(candidate)
    with st.container(border=True):
        person_column, score_column, action_column = st.columns([3.2, 1, 1])
        with person_column:
            role = (
                candidate.get("role")
                or candidate.get("designation")
                or ""
            )
            experience = candidate.get("experience") or ""
            st.markdown(
                f"""
                <div class="employee-person">
                  <span class="avatar">{escape(initials(str(name)))}</span>
                  <div><strong>{rank}. {escape(str(name))}</strong>
                  <small>{escape(str(role))}
                  {f" · {escape(str(experience))}" if experience else ""}</small></div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if skills_value:
                st.markdown(chips(skills_value, limit=8), unsafe_allow_html=True)
            breakdown_parts = []
            for label, key in (
                ("Requirements", "requirements"),
                ("Role", "role"),
                ("Experience", "experience"),
                ("Semantic", "semantic"),
            ):
                value = score_breakdown.get(key)
                if isinstance(value, (int, float)):
                    breakdown_parts.append(f"{label} {value:.0f}%")
            if breakdown_parts:
                st.caption(" · ".join(breakdown_parts))
            if missing_requirements:
                st.caption(
                    "Missing requirements: "
                    + ", ".join(
                        str(value)
                        for value in missing_requirements
                    )
                )
            evidence_parts = [
                f"{item.get('requirement')}: {item.get('level')}"
                for item in requirement_evidence
                if item.get("requirement")
                and item.get("level") != "Not found"
            ]
            if evidence_parts:
                st.caption("Evidence · " + " · ".join(evidence_parts))
            if candidate.get("reason"):
                st.caption(str(candidate["reason"]))
        with score_column:
            st.metric(
                "Job fit",
                f"{score:.1f}%" if score is not None else "Not scored",
            )
            score_band = str(candidate.get("score_band") or "")
            if score_band:
                band_color = {
                    "Strong": "green",
                    "Good": "blue",
                    "Partial": "orange",
                    "Low": "red",
                }.get(score_band, "gray")
                st.badge(
                    f"{score_band} fit",
                    color=band_color,
                )
        with action_column:
            if employee_id and st.button(
                "View Profile",
                key=(
                    f"assistant_profile_{widget_scope}_"
                    f"{rank}_{employee_id}"
                ),
                width="stretch",
            ):
                st.session_state.selected_employee_id = int(employee_id)
                st.switch_page("pages/2_Employee_360.py")


def render_answer(
    response: dict[str, Any],
    message_index: int,
) -> None:
    answer = response.get("answer")
    intent = str(response.get("intent") or "")

    if intent.upper() == "SEARCH" and isinstance(answer, dict):
        candidates = ranked_candidates(answer)
        if candidates:
            st.markdown(f"**Top matches ({len(candidates)})**")
            for index, candidate in enumerate(candidates, start=1):
                render_candidate(
                    candidate,
                    index,
                    widget_scope=f"message_{message_index}",
                )
            recommendation = answer.get("recommendation")
            if recommendation:
                st.info(str(recommendation))
            disclaimer = answer.get("disclaimer")
            if disclaimer:
                st.caption(str(disclaimer))
        else:
            recommendation = (
                answer.get("recommendation")
                or "No employee met the required match threshold."
            )
            query = answer.get("query")
            query_html = (
                '<div class="no-match-query">'
                f'Searched for: “{escape(str(query))}”'
                "</div>"
                if query
                else ""
            )
            st.html(
                f"""
                <div class="assistant-no-match">
                  <div class="no-match-icon">?</div>
                  <div class="no-match-content">
                    <div class="no-match-eyebrow">Search completed</div>
                    <h4>No suitable candidates found</h4>
                    <p>{escape(str(recommendation))}</p>
                    {query_html}
                    <div class="no-match-tip">
                      Try a broader skill, remove one requirement, or lower
                      the experience constraint.
                    </div>
                  </div>
                </div>
                """
            )
            disclaimer = answer.get("disclaimer")
            if disclaimer:
                st.caption(str(disclaimer))
        return

    if (
        intent.upper() == "SUMMARY"
        and isinstance(answer, str)
        and render_employee_summary(
            response,
            answer,
            message_index,
        )
    ):
        return

    if isinstance(answer, str):
        st.markdown(answer)
    elif answer is not None:
        st.json(answer)
    else:
        st.write("No answer was returned.")


page_header(
    "ESIRA Assistant",
    "Semantic workforce search across ChromaDB, verified against PostgreSQL",
)

history_column, chat_column, sources_column = st.columns([1.05, 3.2, 1.15])

with history_column:
    with st.container(
        border=True,
        key="assistant_history_panel",
    ):
        if st.button(
            "New conversation",
            icon=":material/add:",
            type="primary",
            width="stretch",
        ):
            if st.session_state.esira_messages:
                first_question = next(
                    (
                        item["content"]
                        for item in st.session_state.esira_messages
                        if item["role"] == "user"
                    ),
                    "Conversation",
                )
                st.session_state.esira_conversations.insert(
                    0,
                    str(first_question)[:70],
                )
            st.session_state.esira_messages = []
            st.rerun()

        st.markdown("##### Recent")
        if st.session_state.esira_conversations:
            for index, title in enumerate(
                st.session_state.esira_conversations[:8]
            ):
                st.markdown(
                    f'<div class="chat-source"><strong>◌ '
                    f"{escape(title)}</strong></div>",
                    unsafe_allow_html=True,
                )
        elif st.session_state.esira_messages:
            questions = [
                item["content"]
                for item in st.session_state.esira_messages
                if item["role"] == "user"
            ]
            for title in questions[-6:][::-1]:
                st.markdown(
                    f'<div class="chat-source"><strong>◌ '
                    f"{escape(str(title)[:70])}</strong></div>",
                    unsafe_allow_html=True,
                )
        else:
            st.caption("Your recent searches will appear here.")

with chat_column:
    badge_left, badge_right = st.columns(2)
    badge_left.markdown(
        source_badge("ChromaDB Resume Intelligence", "chroma"),
        unsafe_allow_html=True,
    )
    badge_right.markdown(
        source_badge("PostgreSQL Employee Data", "postgres"),
        unsafe_allow_html=True,
    )

    if not st.session_state.esira_messages:
        with st.container(border=True):
            empty_state(
                "Ask about your workforce",
                "Find employees by skills, projects, training, "
                "certifications, location, availability, or experience.",
                "✦",
            )

    for message_index, message in enumerate(
        st.session_state.esira_messages
    ):
        avatar = (
            ":material/person:"
            if message["role"] == "user"
            else ":material/smart_toy:"
        )
        with st.chat_message(message["role"], avatar=avatar):
            if message["role"] == "assistant":
                render_answer(
                    message["content"],
                    message_index,
                )
            else:
                st.markdown(message["content"])

    st.markdown("##### Suggested searches")
    suggestions = (
        "Find FastAPI developers with Docker experience",
        "Show available employees with AWS certification",
        "Summarize employee 1045",
        "Compare employees 1045 and 1089",
    )
    selected_prompt = None
    for row_start in range(0, len(suggestions), 2):
        prompt_columns = st.columns(2)
        for column, suggestion in zip(
            prompt_columns,
            suggestions[row_start:row_start + 2],
        ):
            if column.button(
                suggestion,
                key=f"suggestion_{suggestion}",
                width="stretch",
            ):
                selected_prompt = suggestion

with sources_column:
    with st.container(
        border=True,
        key="assistant_sources_panel",
    ):
        st.markdown("##### Sources Used")
        st.markdown(
            f"""
            <div class="chat-source">
              <strong>{source_badge("ChromaDB", "chroma")}</strong>
              <p>Semantic resume chunks, skills, projects, training, and certifications</p>
            </div>
            <div class="chat-source">
              <strong>{source_badge("PostgreSQL", "postgres")}</strong>
              <p>Employee identity, status, availability, and resume metadata</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("##### Query Plan")
        st.markdown(
            """
            <div class="plan-step"><strong>1 · Semantic Search</strong>
            <span>Retrieve matching resume chunks from ChromaDB.</span></div>
            <div class="plan-step"><strong>2 · Employee Verification</strong>
            <span>Verify operational employee data in PostgreSQL.</span></div>
            <div class="plan-step"><strong>3 · Grounded Answer</strong>
            <span>Rank and explain only retrieved results.</span></div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("##### Safety & Privacy")
        st.caption(
            "Enterprise data access should be authorized and logged. "
            "Verify important employment decisions."
        )

question = st.chat_input(
    "Ask about employees, skills, projects, training, or resumes...",
    submit_mode="disable",
)
question = question or selected_prompt

if question:
    st.session_state.esira_messages.append(
        {"role": "user", "content": question}
    )
    with st.spinner("Searching resume intelligence and verifying employees..."):
        try:
            response = service.ask(question)
        except APIError as ex:
            response = {
                "intent": "ERROR",
                "content_type": "text",
                "answer": str(ex),
            }
    st.session_state.esira_messages.append(
        {"role": "assistant", "content": response}
    )
    st.rerun()
