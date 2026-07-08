from pydantic import BaseModel


class AIQueryRequest(BaseModel):

    question: str

class AIQueryResponse(BaseModel):

    answer: str    