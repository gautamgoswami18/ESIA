from __future__ import annotations

from html import escape
from pathlib import Path
from typing import Any, Iterable

import streamlit as st


UI_DIR = Path(__file__).resolve().parents[1]
STYLE_PATH = UI_DIR / "assets" / "styles.css"

NAV_ITEMS = (
    ("app.py", "Overview", ":material/dashboard:"),
    ("pages/1_Employees.py", "Employees", ":material/groups:"),
    (
        "pages/2_Employee_360.py",
        "Employee 360",
        ":material/account_circle:",
    ),
    (
        "pages/3_AI_Knowledge_Studio.py",
        "AI Knowledge Studio",
        ":material/auto_awesome:",
    ),
    (
        "pages/4_Knowledge_Status.py",
        "Knowledge Status",
        ":material/database:",
    ),
    (
        "pages/5_ESIRA_Assistant.py",
        "ESIRA Assistant",
        ":material/forum:",
    ),
)


def configure_page(title: str, active: str) -> None:
    st.set_page_config(
        page_title=f"{title} · ESIA",
        page_icon="◈",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(
        f"<style>{STYLE_PATH.read_text(encoding='utf-8')}</style>",
        unsafe_allow_html=True,
    )
    render_sidebar(active)


def render_sidebar(active: str) -> None:
    with st.sidebar:
        st.markdown(
            """
            <div class="esia-brand">
                <span class="esia-brand-mark">◈</span>
                <span>ESIA</span>
            </div>
            <div class="esia-nav-label">WORKFORCE INTELLIGENCE</div>
            """,
            unsafe_allow_html=True,
        )
        for page, label, icon in NAV_ITEMS:
            st.page_link(page, label=label, icon=icon)

        st.markdown('<div class="sidebar-spacer"></div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="source-status">
              <div><span class="status-dot"></span> PostgreSQL</div>
              <small>Operational metadata</small>
            </div>
            <div class="source-status">
              <div><span class="status-dot teal"></span> ChromaDB AI</div>
              <small>Resume intelligence</small>
            </div>
            <div class="admin-card">
              <span class="avatar avatar-small">AD</span>
              <div><strong>Admin User</strong><small>Administrator</small></div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def page_header(
    title: str,
    subtitle: str = "",
    eyebrow: str | None = None,
) -> None:
    eyebrow_html = (
        f'<div class="page-eyebrow">{escape(eyebrow)}</div>'
        if eyebrow
        else ""
    )
    subtitle_html = (
        f'<p class="page-subtitle">{escape(subtitle)}</p>'
        if subtitle
        else ""
    )
    st.markdown(
        f"""
        <div class="page-heading">
          {eyebrow_html}
          <h1>{escape(title)}</h1>
          {subtitle_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def source_badge(label: str, source: str = "postgres") -> str:
    kind = "chroma" if source.lower().startswith("chroma") else "postgres"
    icon = "◉" if kind == "chroma" else "♙"
    return (
        f'<span class="source-badge {kind}">'
        f"{icon} {escape(label)}</span>"
    )


def metric_card(
    label: str,
    value: Any,
    icon: str,
    source: str = "PostgreSQL",
    tone: str = "blue",
    detail: str = "",
) -> None:
    safe_value = "—" if value is None else escape(str(value))
    badge_source = "chroma" if "chroma" in source.lower() else "postgres"
    st.markdown(
        f"""
        <div class="metric-card-enterprise">
          <div class="metric-top">
            <span class="metric-icon {escape(tone)}">{escape(icon)}</span>
            <span class="metric-label">{escape(label)}</span>
          </div>
          <div class="metric-value">{safe_value}</div>
          <div class="metric-footer">
            {source_badge(source, badge_source)}
            <span>{escape(detail)}</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def status_pill(value: Any) -> str:
    text = str(value or "Unknown")
    lowered = text.lower()
    if lowered in {"active", "available", "yes", "success", "indexed", "true"}:
        tone = "success"
    elif lowered in {"pending", "on leave", "bench", "notice"}:
        tone = "warning"
    elif lowered in {"failed", "inactive", "no", "false"}:
        tone = "danger"
    else:
        tone = "neutral"
    return f'<span class="status-pill {tone}">{escape(text)}</span>'


def chips(items: Iterable[Any], limit: int | None = None) -> str:
    values = list(items)
    if limit is not None:
        values = values[:limit]
    parts = []
    for item in values:
        if isinstance(item, dict):
            label = (
                item.get("name")
                or item.get("skill_name")
                or item.get("technology")
                or ""
            )
        else:
            label = str(item)
        if label and label.strip(" -"):
            parts.append(f'<span class="chip">{escape(label)}</span>')
    return "".join(parts)


def empty_state(title: str, message: str, icon: str = "◇") -> None:
    st.markdown(
        f"""
        <div class="empty-state">
          <div class="empty-icon">{escape(icon)}</div>
          <strong>{escape(title)}</strong>
          <p>{escape(message)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def safe_name(employee: dict) -> str:
    return (
        f"{employee.get('first_name') or ''} "
        f"{employee.get('last_name') or ''}"
    ).strip() or "Unnamed employee"


def initials(name: str) -> str:
    parts = [part for part in name.split() if part]
    return "".join(part[0].upper() for part in parts[:2]) or "ES"


def unwrap_data(payload: dict | None, default=None):
    if not payload:
        return default
    if "data" in payload:
        return payload.get("data", default)
    return payload
