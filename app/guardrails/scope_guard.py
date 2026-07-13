from app.guardrails.guardrail_result import GuardrailResult


class ScopeGuard:

    KEYWORDS = [

        "employee",

        "candidate",

        "resume",

        "developer",

        "engineer",

        "java",

        "python",

        "react",

        "spring",

        "skill",

        "training",

        "compare",

        "summary",

        "interview",

        "search",

        "find",

        "backend",

        "frontend",

        "devops",

        "ai"
    ]

    GREETINGS = [

        "hi",

        "hello",

        "hey",

        "good morning",

        "good evening",

        "how are you"
    ]

    @classmethod
    def validate(
        cls,
        question: str
    ) -> GuardrailResult:

        question = question.lower()

        if any(keyword in question for keyword in cls.KEYWORDS):

            return GuardrailResult(True)

        if any(greeting in question for greeting in cls.GREETINGS):

            return GuardrailResult(True)

        return GuardrailResult(

            allowed=False,

            message="I can answer only Employee Skill Intelligence related questions."
        )