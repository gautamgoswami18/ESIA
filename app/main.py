from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError

from app.core.settings import settings
from app.core.logging import logger

from app.api.health import router as health_router
from app.api.employee import router as employee_router
from app.api import resume
from pydantic import ValidationError

from app.middleware.request_logger import RequestLoggingMiddleware
from app.middleware.error_handler import (
    http_exception_handler,
    validation_exception_handler,
    pydantic_validation_exception_handler,
    global_exception_handler
)

# ------------------------------------------------------------------
# Create FastAPI Application
# ------------------------------------------------------------------

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

# ------------------------------------------------------------------
# Middleware
# ------------------------------------------------------------------

app.add_middleware(RequestLoggingMiddleware)

# ------------------------------------------------------------------
# Global Exception Handlers
# ------------------------------------------------------------------

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler,
)
app.add_exception_handler(
    ValidationError,
    pydantic_validation_exception_handler
)

app.add_exception_handler(
    HTTPException,
    http_exception_handler,
)

app.add_exception_handler(
    Exception,
    global_exception_handler,
)
async def global_exception_handler(
    request: Request,
    exc: Exception,
):
    print("=" * 80)
    print(type(exc))
    print(repr(exc))
    print("=" * 80)

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

# ------------------------------------------------------------------
# Routers
# ------------------------------------------------------------------

app.include_router(health_router)
app.include_router(employee_router)
app.include_router(resume.router)

# ------------------------------------------------------------------
# APIs
# ------------------------------------------------------------------

@app.get("/version")
def version():
    return {
        "version": settings.APP_VERSION
    }

# ------------------------------------------------------------------
# Startup Event
# ------------------------------------------------------------------

@app.on_event("startup")
async def startup():

    logger.info("=" * 70)
    logger.info("ESIA Application Started")
    logger.info("=" * 70)

# ------------------------------------------------------------------
# Shutdown Event
# ------------------------------------------------------------------

@app.on_event("shutdown")
async def shutdown():

    logger.info("=" * 70)
    logger.info("ESIA Application Stopped")
    logger.info("=" * 70)