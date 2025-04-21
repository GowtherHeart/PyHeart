from typing import Generic, TypeVar

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from pydantic import BaseModel

T = TypeVar("T")


class DefaultResponseModel(BaseModel, Generic[T]):
    payload: T | None = None
    status_code: int = 200
    exception: dict | None = None


class MasterRoute(APIRoute):
    def get_route_handler(self):
        original_handler = super().get_route_handler()

        async def custom_handler(request):
            response = await original_handler(request)
            wrapped = DefaultResponseModel(
                payload=response.custom_content,  # type: ignore
                status_code=response.status_code,
                exception={},
            )
            return JSONResponse(
                content=jsonable_encoder(wrapped), status_code=response.status_code
            )

        return custom_handler
