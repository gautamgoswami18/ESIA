from typing import Any

from pydantic import BaseModel


class ESIRARequest(BaseModel):
    question: str


class ESIRAResponse(BaseModel):
    intent: str
    content_type: str
    answer: Any