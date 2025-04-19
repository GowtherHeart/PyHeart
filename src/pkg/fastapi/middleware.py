from time import time

from fastapi import Request, Response
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware

from src.pkg.context import get_tx_id, make_tx_id


def RequestLogger(
    url: str,
    method: str,
    state: str,
    status_code: int | None = None,
    time_exec: str | None = None,
    content: bytes | None = None,
) -> None:
    _message = ""

    _message += f"[STATE-{state}]"

    if time_exec is not None:
        _message += f"[Time-{time_exec}]"

    _message += f" URL: {url}, Method: {method}"
    if status_code is not None:
        _message += f", Status-Code: {status_code}"

    if content is not None:
        _message += f", Content: {content}"

    logger.opt(depth=1).info(_message)


class MasterMiddelware(BaseHTTPMiddleware):
    """
    MasterMiddleware is a custom middleware for FastAPI applications.

    This middleware is responsible for generating a transaction ID for each request
    by invoking the make_tx_id function. It then proceeds to call the next middleware
    or endpoint in the request handling chain.
    """

    def __init__(self, app) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next) -> Response:
        make_tx_id()
        start = time()

        with logger.contextualize(request_id=get_tx_id()):
            try:
                RequestLogger(
                    url=request.url.__str__(), state="OPEN", method=request.method
                )
                response = await call_next(request)
                return response

            finally:
                time_diff = time() - start
                RequestLogger(
                    url=request.url.__str__(),
                    state="CLOSE",
                    method=request.method,
                    time_exec=str(time_diff),
                )
