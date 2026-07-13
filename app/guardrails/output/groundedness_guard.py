from app.guardrails.guardrail_result import GuardrailResult


class GroundednessGuard:

    @classmethod
    def validate(
        cls,
        answer,
        context
    ):

        if not context:

            return GuardrailResult(
                False,
                "Retrieved context is empty."
            )

        return GuardrailResult(True)