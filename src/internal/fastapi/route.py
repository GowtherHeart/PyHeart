from typing import Generic, TypeVar

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from pydantic import BaseModel

T = TypeVar("T")


class MasterResponseModel(BaseModel, Generic[T]):
    """
    A generic response model for wrapping API responses.

    Attributes:
        payload (T | None): The main content of the response, which can be of any type.
        status_code (int): The HTTP status code of the response. Defaults to 200.
        exception (dict | None): An optional dictionary to include any exception details if present.
    """

    payload: T | None = None
    status_code: int = 200
    exception: dict | None = None


class MasterRoute(APIRoute):
    """
    A custom route class that extends FastAPI's APIRoute to wrap responses in a MasterResponseModel.

    This class overrides the default route handler to ensure that all responses are encapsulated
    within a standardized response model, which includes the payload, status code, and any exception details.

    Methods:
        get_route_handler: Returns a custom route handler that wraps the response in a MasterResponseModel.
    """

    def get_route_handler(self):
        original_handler = super().get_route_handler()

        async def custom_handler(request):
            response = await original_handler(request)
            wrapped = MasterResponseModel(
                payload=response.custom_content,  # type: ignore
                status_code=response.status_code,
                exception={},
            )
            return JSONResponse(
                content=jsonable_encoder(wrapped), status_code=response.status_code
            )

        return custom_handler
