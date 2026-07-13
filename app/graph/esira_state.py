from typing import TypedDict, Optional, Any


class ESIRAState(TypedDict):
    question: str
    intent: str
    answer: Any
    content_type: str
    employee1: Optional[int]
    employee2: Optional[int]
    guard_passed: bool
    guard_message: str
    context: Any
    output_guard_passed: bool
    output_guard_message: str