import argparse
import functools
import types
from enum import Enum
from typing import Sequence

from fastapi import APIRouter, params


class Singleton(type):
    _map: dict = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._map:
            cls._map[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._map[cls]


class Controller:
    """
    Base class for defining controllers. This class is intended to be subclassed
    by specific controller implementations. It provides a common interface and
    structure for controllers, but does not implement any functionality itself.
    """

    name: str = NotImplemented


class EndpointException(Exception): ...


def router(
    path: str,
    status_code: int,
    tags: Sequence[str] | None = None,
    description: str | None = None,
    response_description: str | None = None,
    deprecated: bool | None = None,
    responses=None,
):
    """
    Decorator to define a route for an HTTP endpoint in a FastAPI application.

    Args:
        path (str): The URL path for the endpoint.
        status_code (int): The HTTP status code to be returned by the endpoint.
        tags (Sequence[str] | None, optional): Tags to categorize the endpoint. Defaults to None.
        description (str | None, optional): A brief description of the endpoint. Defaults to None.
        response_description (str, optional): A description of the response. Defaults to None.
        deprecated (bool | None, optional): Indicates if the endpoint is deprecated. Defaults to None.
        responses (optional): Additional response models and descriptions. Defaults to None.

    Returns:
        function: A decorator that wraps the endpoint function with additional metadata.
    """

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)

        wrapper.data = {  # type: ignore
            "path": path,
            "status_code": status_code,
            "tags": tags,
            "description": description,
            "response_description": response_description,
            "deprecated": deprecated,
            "responses": responses,
        }
        wrapper.core_func = func  # type: ignore
        return wrapper

    return decorator


class HttpController(Controller, metaclass=Singleton):
    """
    HttpController is a base class for creating HTTP controllers in a FastAPI application.
    It provides a structure for defining HTTP endpoints with common HTTP methods such as GET, POST, DELETE, PUT, and PATCH.
    This class uses a Singleton pattern to ensure a single instance and automatically registers routes based on the methods implemented in subclasses.
    """

    prefix: str
    tags: list[str | Enum] | None = None
    dependencies: list[params.Depends] | None = None
    deprecated: bool | None = None

    def __build(self, method: str) -> None:
        func = getattr(self, method)
        data = func.data.copy()
        setattr(self, method, types.MethodType(func.core_func, self))
        self.router.add_api_route(
            path=data["path"],
            endpoint=getattr(self, method),
            status_code=data["status_code"],
            tags=data["tags"],
            description=data["description"],
            response_description=data["response_description"],
            deprecated=data["deprecated"],
            responses=data["responses"],
            methods=[method.upper()],
        )

    def __init__(self) -> None:
        self.router = APIRouter(
            prefix=self.prefix,
            tags=self.tags,
            dependencies=self.dependencies,
            deprecated=self.deprecated,
        )

        _method = type(self).get
        if _method is not HttpController.get:
            self.__build(method="get")

        _method = type(self).post
        if _method is not HttpController.post:
            self.__build(method="post")

        _method = type(self).delete
        if _method is not HttpController.delete:
            self.__build(method="delete")

        _method = type(self).put
        if _method is not HttpController.put:
            self.__build(method="put")

        _method = type(self).patch
        if _method is not HttpController.patch:
            self.__build(method="patch")

    async def get(self):
        raise EndpointException()

    async def post(self):
        raise EndpointException()

    async def delete(self):
        raise EndpointException()

    async def put(self):
        raise EndpointException()

    async def patch(self):
        raise EndpointException()


class CliController(Controller, metaclass=Singleton):
    """
    CliController is a base class for creating command-line interface (CLI) controllers.
    It provides a structure for defining CLI commands and arguments using argparse.
    This class uses a Singleton pattern to ensure a single instance and automatically
    parses command-line arguments based on the specified args attribute.
    """

    args: list[str]

    def __init__(self) -> None:
        parser = argparse.ArgumentParser()
        for el in self.args:
            parser.add_argument(f"--{el}", required=True)

        self.data, _ = parser.parse_known_args()

    async def run(self, *args, **kwargs):
        await self.execute(*args, **kwargs)

    async def execute(self) -> None:
        raise NotImplementedError()
