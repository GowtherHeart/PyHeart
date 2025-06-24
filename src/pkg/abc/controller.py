import argparse
import functools
import types
from enum import Enum
from typing import Sequence

from fastapi import APIRouter, Response, params
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute


class Singleton(type):
    """Metaclass for implementing the Singleton design pattern."""

    _map: dict = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._map:
            cls._map[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._map[cls]


class Controller:
    """Abstract base class for all controller implementations."""

    name: str = NotImplemented


class EndpointException(Exception):
    """Exception raised when an HTTP endpoint is not implemented."""

    ...


class DocsInitException(Exception):
    """Exception raised during API documentation initialization."""

    ...


def router(
    path: str,
    status_code: int,
    tags: Sequence[str] | None = None,
    description: str | None = None,
    response_description: str | None = None,
    deprecated: bool | None = None,
    response_class: type[Response] | None = None,
    responses=None,
    response_model=None,
):
    """Decorator to define a route for an HTTP endpoint in a FastAPI application."""

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
            "responses": responses if responses is not None else {},
            "response_class": response_class,
            "response_model": response_model,
        }
        wrapper.core_func = func  # type: ignore
        return wrapper

    return decorator


class HttpController(Controller, metaclass=Singleton):
    """Base singleton class for HTTP API controllers using FastAPI."""

    prefix: str
    tags: list[str | Enum] | None = None
    dependencies: list[params.Depends] | None = None
    deprecated: bool | None = None
    response_class: type[Response] | None = None
    route_class: type[APIRoute] | None = None

    def __build(self, method: str) -> None:
        func = getattr(self, method)
        data = func.data.copy()
        setattr(self, method, types.MethodType(func.core_func, self))

        _response_class: type[Response]
        if data["response_class"] is not None:
            _response_class = data["response_class"]
        elif self.response_class is not None:
            _response_class = self.response_class
        else:
            _response_class = JSONResponse

        _responses = data["responses"].copy()
        if (
            data["response_model"] is not None
            and self.route_class is not None
            and "local_response_model_field_map" in self.route_class.__dict__
        ):
            field_map = {}
            for k, v in self.route_class.local_response_model_field_map.items():  # type: ignore
                _v = data.get(v, None)
                if _v is None:
                    raise DocsInitException()

                field_map[k] = _v

            _responses[data["status_code"]] = {
                "content": {
                    "application/json": {
                        "example": self.route_class.local_response_model(  # type: ignore
                            **field_map
                        )
                    }
                }
            }

        self.router.add_api_route(
            path=data["path"],
            endpoint=getattr(self, method),
            status_code=data["status_code"],
            tags=data["tags"],
            description=data["description"],
            response_description=data["response_description"],
            deprecated=data["deprecated"],
            responses=_responses,
            methods=[method.upper()],
            response_class=_response_class,
        )

    def __init__(self) -> None:
        self.router = APIRouter(
            prefix=self.prefix,
            tags=self.tags,
            dependencies=self.dependencies,
            deprecated=self.deprecated,
            route_class=self.route_class if self.route_class is not None else APIRoute,
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
    """Base singleton class for command-line interface controllers."""

    args: list[str]

    def __init__(self) -> None:
        parser = argparse.ArgumentParser()
        for el in self.args:
            parser.add_argument(f"--{el}", required=True)

        self.data, _ = parser.parse_known_args()

    async def run(self, *args, **kwargs):
        await self.execute(*args, **kwargs)

    async def execute(self) -> None:
        """Execute the CLI command logic."""
        raise NotImplementedError()
