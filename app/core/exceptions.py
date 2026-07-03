from fastapi import HTTPException


class ResourceNotFoundException(HTTPException):

    def __init__(self, resource: str):

        super().__init__(
            status_code=404,
            detail=f"{resource} not found"
        )


class BadRequestException(HTTPException):

    def __init__(self, message: str):

        super().__init__(
            status_code=400,
            detail=message
        )


class DatabaseException(HTTPException):

    def __init__(self):

        super().__init__(
            status_code=500,
            detail="Database Error"
        )