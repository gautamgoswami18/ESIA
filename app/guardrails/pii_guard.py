import re

from app.guardrails.guardrail_result import GuardrailResult


class PIIGuard:

    EMAIL = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

    PHONE = r"\b\d{10}\b"

    @classmethod
    def validate(
        cls,
        question: str
    ) -> GuardrailResult:

        if re.search(cls.EMAIL, question):

            return GuardrailResult(

                allowed=False,

                message="Email addresses are not allowed."
            )

        if re.search(cls.PHONE, question):

            return GuardrailResult(

                allowed=False,

                message="Phone numbers are not allowed."
            )

        return GuardrailResult(True)