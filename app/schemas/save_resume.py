from pydantic import BaseModel


class SaveResumeRequest(BaseModel):

    process_id: str