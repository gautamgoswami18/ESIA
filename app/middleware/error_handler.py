from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from loguru import logger
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError

from app.schemas.response import APIResponse


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
# FastAPI Request Validation Exceptions
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
           data=jsonable_encoder(exc.errors()),
        ).model_dump()
    )


# ------------------------------------------------------------------
# Pydantic Model Validation Exceptions
# ------------------------------------------------------------------

async def pydantic_validation_exception_handler(
    request: Request,
    exc: ValidationError,
):
    return JSONResponse(
        status_code=422,
        content=APIResponse(
            success=False,
            message="Validation Error",
            data=jsonable_encoder(exc.errors()),
        ).model_dump()
    )


# ------------------------------------------------------------------
# Global Exception Handler
# ------------------------------------------------------------------

async def global_exception_handler(
    request: Request,
    exc: Exception,
):
  
    raise exc
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