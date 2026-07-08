from pydantic import BaseModel


class ESIRARequest(BaseModel):

    question: str


class ESIRAResponse(BaseModel):

    answer: str