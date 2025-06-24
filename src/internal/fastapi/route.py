from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute

from .model import MasterResponseModel


class MasterRoute(APIRoute):
    """Custom route class that wraps responses in a MasterResponseModel."""

    local_response_model = MasterResponseModel
    local_response_model_field_map = {
        "payload": "response_model",
        "status_code": "status_code",
    }

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
