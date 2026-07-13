from app.guardrails.guardrail_result import GuardrailResult


class HallucinationGuard:

    @classmethod
    def validate(
        cls,
        answer,
        context
    ):

        if answer is None:

            return GuardrailResult(
                False,
                "No answer generated."
            )

        if context is None:

            return GuardrailResult(
                False,
                "No context available."
            )

        return GuardrailResult(True)