import json

from app.guardrails.guardrail_result import GuardrailResult


class JSONGuard:

    @classmethod
    def validate(
        cls,
        response
    ):

        if response is None:

            return GuardrailResult(
                False,
                "LLM returned empty response."
            )

        if isinstance(response, dict):

            return GuardrailResult(True)

        try:

            json.loads(response)

            return GuardrailResult(True)

        except Exception:

            return GuardrailResult(
                False,
                "Invalid JSON generated."
            )