from math import ceil

from pydantic import BaseModel


class Pagination(BaseModel):
    page: int
    size: int
    total_records: int
    total_pages: int

    @classmethod
    def create(
        cls,
        page: int,
        size: int,
        total_records: int
    ) -> "Pagination":
        return cls(
            page=page,
            size=size,
            total_records=total_records,
            total_pages=ceil(total_records / size) if size > 0 else 0
        )