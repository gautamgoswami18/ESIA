from app.schemas.api_response import ApiResponse, PaginatedResponse


def success_response(data=None, message="Success"):
    return ApiResponse(
        success=True,
        message=message,
        data=data
    )


def paginated_response(
    data,
    total,
    page,
    size,
    message="Success"
):
    return PaginatedResponse(
        success=True,
        message=message,
        page=page,
        size=size,
        total=total,
        data=data
    )