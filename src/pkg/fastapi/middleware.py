from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from src.pkg.context import make_tx_id


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
        response = await call_next(request)
        return response
