from typing import Any

from fastapi import HTTPException


class CoreException(HTTPException):
    """
    CoreException is a custom exception class that extends FastAPI's HTTPException.
    It allows for defining a specific status code and detail message for HTTP errors
    that occur within the application. This class can be used as a base class for
    more specific exceptions that require HTTP status codes and detailed error messages.
    """

    status_code: Any = ...
    detail: Any = ...

    def __init__(self) -> None:
        super().__init__(status_code=self.status_code, detail=self.detail)
