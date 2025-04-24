from contextlib import asynccontextmanager
from typing import AsyncGenerator

from httpx import ASGITransport, AsyncClient

from tests.pkg.apps import HttpApp

__all__ = ["get_client"]


@asynccontextmanager
async def get_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=HttpApp().app()), base_url="http://testserver") as client:  # type: ignore
        yield client
