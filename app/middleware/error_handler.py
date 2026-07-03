from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.schemas.response import APIResponse
from app.core.logging import logger


# ------------------------------------------------------------------
# HTTP Exceptions
# ------------------------------------------------------------------

async def http_exception_handler(
    request: Request,
    exc: HTTPException,
):
    return JSONResponse(
        status_code=exc.status_code,
        content=APIResponse(
            success=False,
            message=exc.detail,
            data=None,
        ).model_dump()
    )


# ------------------------------------------------------------------
# Validation Exceptions
# ------------------------------------------------------------------

async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    return JSONResponse(
        status_code=422,
        content=APIResponse(
            success=False,
            message="Validation Error",
            data=exc.errors(),
        ).model_dump()
    )


# ------------------------------------------------------------------
# Global Exception Handler
# ------------------------------------------------------------------

async def global_exception_handler(
    request: Request,
    exc: Exception,
):
    logger.exception(
        f"Unhandled exception while processing "
        f"{request.method} {request.url.path}"
    )

    return JSONResponse(
        status_code=500,
        content=APIResponse(
            success=False,
            message="Internal Server Error",
            data=None,
        ).model_dump()
    )