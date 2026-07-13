from app.guardrails.guardrail_result import GuardrailResult


class PromptInjectionGuard:

    BLOCKED_PATTERNS = [

        "ignore previous instructions",

        "forget previous instructions",

        "system prompt",

        "reveal prompt",

        "act as",

        "bypass",

        "jailbreak",

        "developer mode",

        "pretend you are",

        "override",

        "disable guard",

        "ignore all"
    ]

    @classmethod
    def validate(
        cls,
        question: str
    ) -> GuardrailResult:

        question = question.lower()

        for pattern in cls.BLOCKED_PATTERNS:

            if pattern in question:

                return GuardrailResult(

                    allowed=False,

                    message="Prompt Injection detected."
                )

        return GuardrailResult(True)