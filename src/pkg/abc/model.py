from pydantic import BaseModel


class DbModel(BaseModel):
    """Base Pydantic model for database operations and data persistence."""


class ParamsModel(BaseModel):
    """Base Pydantic model for HTTP request parameters and query parameters."""


class PayloadModel(BaseModel):
    """Base Pydantic model for HTTP request payloads and body data."""


class ResponseModel(BaseModel):
    """Base Pydantic model for HTTP response data and API responses."""


class Model(BaseModel):
    """Generic base Pydantic model for general-purpose data structures."""

    ...
