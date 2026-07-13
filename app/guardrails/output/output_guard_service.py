from app.guardrails.output.json_guard import JSONGuard
from app.guardrails.output.hallucination_guard import HallucinationGuard
from app.guardrails.output.groundedness_guard import GroundednessGuard
from app.guardrails.output.pii_mask_guard import PIIMaskGuard
from app.guardrails.output.no_result_guard import NoResultGuard

class OutputGuardService:

    @classmethod
    def validate(cls, answer, context=None):

        result = NoResultGuard.validate(answer)

        if result and not result.allowed:
            return result

        result = JSONGuard.validate(answer)

        if result and not result.allowed:
            return result

        result = HallucinationGuard.validate(
            answer,
            context
        )

        if result and not result.allowed:
            return result

        result = GroundednessGuard.validate(
            answer,
            context
        )

        if result and not result.allowed:
            return result

        return None
    
    @classmethod
    def sanitize(
        cls,
        answer
    ):

        return PIIMaskGuard.sanitize(answer)