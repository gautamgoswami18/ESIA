from __future__ import annotations

import json
from typing import Any


def build_ranked_context(candidates: list[dict[str, Any]]) -> str:
    """Serialize canonical candidates for the explanation-only LLM step."""
    context_candidates = []
    for candidate in candidates:
        context_candidates.append(
            {
                "rank": candidate["rank"],
                "employee_id": candidate["employee_id"],
                "name": candidate["name"],
                "role": candidate["role"],
                "experience": candidate["experience"],
                "employment_status": candidate.get(
                    "employment_status",
                    "",
                ),
                "availability": candidate.get("availability", ""),
                "match_score": candidate["match_score"],
                "semantic_score": candidate.get("semantic_score", 0),
                "score_band": candidate.get("score_band", ""),
                "score_breakdown": candidate.get(
                    "score_breakdown",
                    {},
                ),
                "required_requirements": candidate.get(
                    "required_requirements",
                    [],
                ),
                "matched_requirements": candidate.get(
                    "matched_requirements",
                    [],
                ),
                "missing_requirements": candidate.get(
                    "missing_requirements",
                    [],
                ),
                "requirement_evidence": candidate.get(
                    "requirement_evidence",
                    [],
                ),
                "requested_role": candidate.get("requested_role"),
                "required_experience_years": candidate.get(
                    "required_experience_years"
                ),
                "resume_context": candidate.get("resume_text", ""),
            }
        )
    return json.dumps(
        {"ranked_candidates": context_candidates},
        ensure_ascii=False,
    )


def ground_search_response(
    question: str,
    candidates: list[dict[str, Any]],
    generated: dict[str, Any] | None,
) -> dict[str, Any]:
    """Keep ranking and identity canonical; accept only LLM explanations."""
    if not candidates:
        return {
            "query": question,
            "best_candidate": None,
            "other_candidates": [],
            "recommendation": "No matching resume was found.",
            "disclaimer": (
                "Decision-support only. A staffing or HR manager must "
                "review the underlying evidence."
            ),
        }

    generated = generated if isinstance(generated, dict) else {}
    generated_candidates = _generated_candidates(generated)
    by_employee_id = {
        str(candidate.get("employee_id")): candidate
        for candidate in generated_candidates
        if candidate.get("employee_id") not in (None, "")
    }
    by_rank = {
        _integer(candidate.get("rank")): candidate
        for candidate in generated_candidates
        if _integer(candidate.get("rank")) is not None
    }

    grounded = []
    for canonical in candidates:
        explanation = (
            by_employee_id.get(str(canonical["employee_id"]))
            or by_rank.get(canonical["rank"])
            or {}
        )
        skills = (
            canonical.get("matched_requirements")
            or explanation.get("matching_skills")
            or []
        )
        if not isinstance(skills, list):
            skills = []

        grounded.append(
            {
                "rank": canonical["rank"],
                "employee_id": canonical["employee_id"],
                "name": canonical["name"]
                or f"Employee {canonical['employee_id']}",
                "role": canonical["role"],
                "experience": canonical["experience"],
                "match_score": canonical["match_score"],
                "semantic_score": canonical.get("semantic_score", 0),
                "score_band": canonical.get("score_band", ""),
                "score_breakdown": canonical.get(
                    "score_breakdown",
                    {},
                ),
                "required_requirements": canonical.get(
                    "required_requirements",
                    [],
                ),
                "matched_requirements": canonical.get(
                    "matched_requirements",
                    [],
                ),
                "missing_requirements": canonical.get(
                    "missing_requirements",
                    [],
                ),
                "requirement_evidence": canonical.get(
                    "requirement_evidence",
                    [],
                ),
                "matching_skills": [
                    str(skill)
                    for skill in skills
                    if skill not in (None, "")
                ][:8],
                "reason": str(explanation.get("reason") or "").strip(),
            }
        )

    best = grounded[0]
    recommendation = (
        f"{best['name']} has the highest job-fit score "
        f"at {best['match_score']}%. Review the evidence and "
        f"identified gaps before making a staffing decision."
    )
    return {
        "query": question,
        "best_candidate": best,
        "other_candidates": grounded[1:],
        "recommendation": recommendation,
        "disclaimer": (
            "Decision-support only. The score uses job-related resume "
            "evidence and must not replace human review."
        ),
    }


def _generated_candidates(generated: dict[str, Any]) -> list[dict]:
    candidates = []
    best = generated.get("best_candidate")
    if isinstance(best, dict):
        candidates.append(best)
    others = generated.get("other_candidates")
    if isinstance(others, list):
        candidates.extend(
            candidate
            for candidate in others
            if isinstance(candidate, dict)
        )
    return candidates


def _integer(value) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None
