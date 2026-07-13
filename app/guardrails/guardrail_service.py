from app.guardrails.prompt_injection_guard import PromptInjectionGuard
from app.guardrails.pii_guard import PIIGuard
from app.guardrails.scope_guard import ScopeGuard
from app.guardrails.toxicity_guard import ToxicityGuard


class GuardrailService:

    @classmethod
    def validate(
        cls,
        question: str
    ):

        guards = [

            PromptInjectionGuard,

            PIIGuard,

            ToxicityGuard,

            ScopeGuard

        ]

        for guard in guards:

            result = guard.validate(question)

            if not result.allowed:

                return result

        return None