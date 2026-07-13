from app.guardrails.guardrail_result import GuardrailResult


class ToxicityGuard:

    BAD_WORDS = [

        "idiot",

        "stupid",

        "fool",

        "hate",

        "kill"
    ]

    @classmethod
    def validate(
        cls,
        question: str
    ) -> GuardrailResult:

        question = question.lower()

        for word in cls.BAD_WORDS:

            if word in question:

                return GuardrailResult(

                    allowed=False,

                    message="Please use respectful language."
                )

        return GuardrailResult(True)