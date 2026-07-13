from dataclasses import dataclass


@dataclass
class GuardrailResult:

    allowed: bool

    message: str = ""