from typing import Any

from pydantic import BaseModel

from app.schemas.pagination import Pagination


class APIResponse(BaseModel):
    success: bool
    message: str
    data: Any = None
    pagination: Pagination | None = None