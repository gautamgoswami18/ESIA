import time

from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logging import logger


class RequestLoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        start = time.time()

        response = await call_next(request)

        duration = round((time.time() - start) * 1000, 2)

        logger.info(
            f"{request.method} "
            f"{request.url.path} "
            f"Status={response.status_code} "
            f"Time={duration}ms"
        )

        return response