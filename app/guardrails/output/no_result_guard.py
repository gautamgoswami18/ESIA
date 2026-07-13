from app.guardrails.guardrail_result import GuardrailResult


class NoResultGuard:

    MIN_MATCH_SCORE = 20

    @classmethod
    def validate(cls, answer):

        if answer is None:
            return GuardrailResult(
                False,
                "No matching employee found."
            )

        # Search response is expected to be a dictionary
        if not isinstance(answer, dict):
            return GuardrailResult(True)

        best = answer.get("best_candidate")

        if best is None:
            return GuardrailResult(
                False,
                "No matching employee found."
            )

        name = best.get("name")

        if not name:
            return GuardrailResult(
                False,
                "No matching employee found."
            )

        score = best.get("match_score", 0)

        if score < cls.MIN_MATCH_SCORE:
            return GuardrailResult(
                False,
                f"No suitable candidate found (Match Score {score}%)."
            )

        return GuardrailResult(True)