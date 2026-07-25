from __future__ import annotations

from html import escape
from typing import Any

import streamlit as st

from api_client import APIError
from components.enterprise_ui import (
    chips,
    configure_page,
    empty_state,
    initials,
    page_header,
    source_badge,
)
from services.workforce_service import WorkforceService


configure_page("ESIRA Assistant", "ESIRA Assistant")
service = WorkforceService()

if "esira_messages" not in st.session_state:
    st.session_state.esira_messages = []
if "esira_conversations" not in st.session_state:
    st.session_state.esira_conversations = []


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
    with st.container(border=True):
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
    prompt_columns = st.columns(3)
    suggestions = (
        "Find FastAPI developers with Docker experience",
        "Show available employees with AWS certification",
        "Who has banking-domain project experience?",
    )
    selected_prompt = None
    for column, suggestion in zip(prompt_columns, suggestions):
        if column.button(
            suggestion,
            key=f"suggestion_{suggestion}",
            width="stretch",
        ):
            selected_prompt = suggestion

with sources_column:
    with st.container(border=True):
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
