from typing import TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class MasterResponseModel[T](BaseModel):
    """Generic response model for wrapping API responses."""

    payload: T | None = None
    status_code: int = 200
    exception: dict | None = None
