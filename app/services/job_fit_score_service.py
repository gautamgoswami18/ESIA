from __future__ import annotations

import re
from typing import Any


class JobFitScoreService:
    """Explainable, job-related scoring over query and resume evidence."""

    STOP_WORDS = {
        "a",
        "about",
        "all",
        "also",
        "an",
        "and",
        "any",
        "are",
        "as",
        "at",
        "available",
        "best",
        "candidate",
        "candidates",
        "certification",
        "certifications",
        "certified",
        "employee",
        "employees",
        "experience",
        "experienced",
        "find",
        "for",
        "good",
        "has",
        "have",
        "in",
        "knowledge",
        "list",
        "now",
        "of",
        "on",
        "or",
        "position",
        "required",
        "resource",
        "resources",
        "role",
        "show",
        "skill",
        "skills",
        "technology",
        "the",
        "top",
        "trained",
        "training",
        "who",
        "with",
        "worked",
        "working",
        "year",
        "years",
        "yrs",
    }

    ROLE_ALIASES = {
        "data scientist": ("data scientist", "data science"),
        "devops engineer": ("devops engineer", "devops"),
        "qa engineer": (
            "qa engineer",
            "quality engineer",
            "test engineer",
            "tester",
        ),
        "architect": ("architect", "solution architect"),
        "manager": ("manager", "engineering manager"),
        "analyst": ("analyst", "business analyst", "data analyst"),
        "developer": (
            "developer",
            "software engineer",
            "application engineer",
            "programmer",
        ),
        "engineer": ("engineer", "developer"),
    }

    PHRASE_REQUIREMENTS = {
        "artificial intelligence": (
            "Artificial Intelligence",
            ("artificial intelligence", "ai"),
        ),
        "machine learning": (
            "Machine Learning",
            ("machine learning", "ml"),
        ),
        "spring boot": ("Spring Boot", ("spring boot",)),
        "power bi": ("Power BI", ("power bi", "powerbi")),
        "rest api": ("REST API", ("rest api", "restful api")),
        "node js": ("Node.js", ("node.js", "nodejs", "node js")),
        "react js": ("React", ("react", "react.js", "reactjs")),
    }

    TOKEN_ALIASES = {
        "ai": ("ai", "artificial intelligence"),
        "ml": ("ml", "machine learning"),
        "aws": ("aws", "amazon web services"),
        ".net": (".net", "dotnet", "asp.net"),
        "dotnet": (".net", "dotnet", "asp.net"),
        "node.js": ("node.js", "nodejs", "node js"),
        "nodejs": ("node.js", "nodejs", "node js"),
        "reactjs": ("react", "react.js", "reactjs"),
    }

    DISPLAY_NAMES = {
        ".net": ".NET",
        "ai": "AI",
        "api": "API",
        "aws": "AWS",
        "c#": "C#",
        "c++": "C++",
        "faiss": "FAISS",
        "fastapi": "FastAPI",
        "git": "Git",
        "html": "HTML",
        "java": "Java",
        "javascript": "JavaScript",
        "ml": "ML",
        "node.js": "Node.js",
        "nodejs": "Node.js",
        "postgresql": "PostgreSQL",
        "python": "Python",
        "react": "React",
        "reactjs": "React",
        "sql": "SQL",
        "typescript": "TypeScript",
    }

    TOKEN_PATTERN = re.compile(
        r"(?<![a-z0-9])"
        r"(?:\.net|c\+\+|c#|[a-z][a-z0-9]*(?:[.-][a-z0-9]+)*)"
        r"(?![a-z0-9])",
        re.IGNORECASE,
    )

    @classmethod
    def score(
        cls,
        query: str,
        candidate: dict[str, Any],
    ) -> dict[str, Any]:
        requirements = cls.extract_requirements(query)
        resume_text = str(candidate.get("resume_text") or "")
        evaluated_requirements = [
            {
                **requirement,
                **cls._evidence_strength(
                    resume_text,
                    requirement["aliases"],
                ),
            }
            for requirement in requirements
        ]
        matched = [
            requirement
            for requirement in evaluated_requirements
            if requirement["score"] > 0
        ]
        missing = [
            requirement
            for requirement in evaluated_requirements
            if requirement["score"] == 0
        ]
        matched_labels = [
            requirement["label"]
            for requirement in matched
        ]
        missing_labels = [
            requirement["label"]
            for requirement in missing
        ]

        semantic_score = cls._bounded(
            candidate.get("semantic_score")
            or candidate.get("match_score")
            or 0
        )
        components = {"semantic": semantic_score}
        weights = {"semantic": 0.25}

        skill_score = None
        if evaluated_requirements:
            skill_score = round(
                sum(
                    requirement["score"]
                    for requirement in evaluated_requirements
                )
                / len(evaluated_requirements),
                1,
            )
            components["requirements"] = skill_score
            weights["requirements"] = 0.60

        requested_role = cls.extract_role(query)
        role_score = None
        if requested_role:
            role_score = cls._role_alignment(
                requested_role,
                str(candidate.get("role") or ""),
                resume_text,
            )
            components["role"] = role_score
            weights["role"] = 0.15

        required_years = cls.extract_required_years(query)
        experience_score = None
        if required_years is not None:
            experience_score = cls._experience_alignment(
                required_years,
                candidate.get("experience_years"),
            )
            components["experience"] = experience_score
            weights["experience"] = 0.15

        weight_total = sum(weights.values())
        fit_score = round(
            sum(
                components[name] * weight
                for name, weight in weights.items()
            )
            / weight_total,
            1,
        )

        return {
            "match_score": cls._bounded(fit_score),
            "semantic_score": semantic_score,
            "score_band": cls._score_band(fit_score),
            "score_breakdown": {
                "requirements": skill_score,
                "role": role_score,
                "experience": experience_score,
                "semantic": semantic_score,
            },
            "required_requirements": [
                requirement["label"]
                for requirement in requirements
            ],
            "matched_requirements": matched_labels,
            "missing_requirements": missing_labels,
            "requirement_evidence": [
                {
                    "requirement": requirement["label"],
                    "level": requirement["level"],
                    "score": requirement["score"],
                }
                for requirement in evaluated_requirements
            ],
            "requested_role": requested_role,
            "required_experience_years": required_years,
            "scoring_method": "hybrid_job_fit_v1",
        }

    @classmethod
    def extract_requirements(
        cls,
        query: str,
    ) -> list[dict[str, Any]]:
        normalized = cls._normalize(query)
        requirements = []
        consumed_tokens = set()

        for phrase, (label, aliases) in cls.PHRASE_REQUIREMENTS.items():
            if cls._contains(normalized, phrase):
                requirements.append(
                    {
                        "key": phrase,
                        "label": label,
                        "aliases": aliases,
                    }
                )
                consumed_tokens.update(phrase.split())

        role_tokens = {
            token
            for aliases in cls.ROLE_ALIASES.values()
            for alias in aliases
            for token in alias.split()
        }
        seen = {requirement["key"] for requirement in requirements}

        for match in cls.TOKEN_PATTERN.finditer(normalized):
            token = match.group(0).casefold()
            if (
                token in consumed_tokens
                or token in cls.STOP_WORDS
                or token in role_tokens
                or token.isdigit()
                or token in seen
            ):
                continue
            if len(token) == 1 and token != "c":
                continue

            requirements.append(
                {
                    "key": token,
                    "label": cls.DISPLAY_NAMES.get(
                        token,
                        token.replace(".", " ").title(),
                    ),
                    "aliases": cls.TOKEN_ALIASES.get(
                        token,
                        (token,),
                    ),
                }
            )
            seen.add(token)

        return requirements

    @classmethod
    def extract_role(cls, query: str) -> str | None:
        normalized = cls._normalize(query)
        for role, aliases in cls.ROLE_ALIASES.items():
            if cls._matches_any(normalized, aliases):
                return role
        return None

    @staticmethod
    def extract_required_years(query: str) -> float | None:
        match = re.search(
            r"(\d+(?:\.\d+)?)\s*(?:\+|plus)?\s*(?:years?|yrs?)",
            query,
            flags=re.IGNORECASE,
        )
        return float(match.group(1)) if match else None

    @classmethod
    def _role_alignment(
        cls,
        requested_role: str,
        designation: str,
        resume_text: str,
    ) -> float:
        aliases = cls.ROLE_ALIASES[requested_role]
        if cls._matches_any(designation, aliases):
            return 100.0

        normalized_designation = cls._normalize(designation)
        if requested_role in {"developer", "engineer"}:
            if cls._matches_any(
                normalized_designation,
                ("technical lead", "team lead"),
            ):
                return 80.0
            if cls._contains(normalized_designation, "architect"):
                return 70.0
            if cls._contains(normalized_designation, "manager"):
                return 50.0

        if cls._matches_any(resume_text, aliases):
            return 65.0
        return 20.0

    @classmethod
    def _evidence_strength(
        cls,
        resume_text: str,
        aliases,
    ) -> dict[str, Any]:
        sections = cls._resume_sections(resume_text)
        if cls._matches_any(sections["experience"], aliases):
            return {"level": "Project/work", "score": 100.0}
        if cls._matches_any(sections["skills"], aliases):
            return {"level": "Skills/summary", "score": 85.0}
        if cls._matches_any(sections["training"], aliases):
            return {
                "level": "Training/certification",
                "score": 60.0,
            }
        if cls._matches_any(resume_text, aliases):
            return {"level": "Resume mention", "score": 70.0}
        return {"level": "Not found", "score": 0.0}

    @staticmethod
    def _resume_sections(resume_text: str) -> dict[str, str]:
        text = str(resume_text or "")
        upper = text.upper()

        def between(start: str, end: str | None) -> str:
            start_index = upper.find(start)
            if start_index < 0:
                return ""
            content_start = start_index + len(start)
            if end is None:
                return text[content_start:]
            end_index = upper.find(end, content_start)
            return text[
                content_start:
                end_index if end_index >= 0 else len(text)
            ]

        return {
            "skills": between(
                "PROFESSIONAL SUMMARY",
                "PROFESSIONAL EXPERIENCE",
            ),
            "experience": between(
                "PROFESSIONAL EXPERIENCE",
                "TRAINING",
            ),
            "training": between("TRAINING", "EDUCATION"),
        }

    @staticmethod
    def _experience_alignment(
        required_years: float,
        candidate_years,
    ) -> float:
        try:
            years = max(0.0, float(candidate_years))
        except (TypeError, ValueError):
            return 0.0
        if required_years <= 0:
            return 100.0
        return round(min(100.0, years / required_years * 100), 1)

    @staticmethod
    def _score_band(score: float) -> str:
        if score >= 80:
            return "Strong"
        if score >= 65:
            return "Good"
        if score >= 50:
            return "Partial"
        return "Low"

    @classmethod
    def _matches_any(
        cls,
        text: str,
        aliases,
    ) -> bool:
        normalized = cls._normalize(text)
        return any(
            cls._contains(normalized, alias)
            for alias in aliases
        )

    @staticmethod
    def _contains(text: str, phrase: str) -> bool:
        return bool(
            re.search(
                rf"(?<![a-z0-9]){re.escape(phrase.casefold())}"
                rf"(?![a-z0-9])",
                text.casefold(),
            )
        )

    @staticmethod
    def _normalize(value: str) -> str:
        return " ".join(str(value or "").casefold().split())

    @staticmethod
    def _bounded(value) -> float:
        try:
            numeric = float(value)
        except (TypeError, ValueError):
            return 0.0
        return round(max(0.0, min(numeric, 100.0)), 1)
