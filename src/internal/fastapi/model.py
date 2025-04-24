from typing import Generic, TypeVar

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
