from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from httpx import ASGITransport, AsyncClient

from tests.pkg.apps import HttpApp

__all__ = ["get_client"]


@asynccontextmanager
async def get_client() -> AsyncGenerator[AsyncClient]:
    async with AsyncClient(
        transport=ASGITransport(app=HttpApp().app()),  # type: ignore
        base_url="http://testserver",  # type: ignore
    ) as client:
        yield client
