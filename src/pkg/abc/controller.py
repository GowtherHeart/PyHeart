import argparse
import functools
import types
from enum import Enum
from typing import Sequence

from fastapi import APIRouter, Response, params
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute


class Singleton(type):
    """Metaclass for implementing the Singleton design pattern.

    This metaclass ensures that only one instance of a class can exist at a time.
    When a class uses this metaclass, subsequent instantiation attempts will
    return the same instance that was created on first instantiation.

    Attributes:
        _map (dict): Internal mapping of classes to their singleton instances.
    """

    _map: dict = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._map:
            cls._map[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._map[cls]


class Controller:
    """Abstract base class for all controller implementations.

    This class serves as the foundation for both HTTP and CLI controllers,
    providing a common interface and structure. Controllers are responsible
    for handling user input, coordinating business logic through use cases,
    and returning appropriate responses.

    Attributes:
        name (str): The name identifier for the controller. Must be implemented
                   by subclasses.

    Note:
        This class should not be instantiated directly. Instead, use one of
        its concrete subclasses like HttpController or CliController.
    """

    name: str = NotImplemented


class EndpointException(Exception):
    """Exception raised when an HTTP endpoint is not implemented or encounters an error.

    This exception is typically raised by the default implementations of HTTP
    methods in HttpController to indicate that a specific endpoint has not been
    implemented by a subclass.
    """

    ...


class DocsInitException(Exception):
    """Exception raised during API documentation initialization.

    This exception occurs when there are issues setting up OpenAPI documentation,
    typically due to missing required metadata or invalid response model
    configurations in HTTP controllers.
    """

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
            "responses": responses if responses is not None else {},
            "response_class": response_class,
            "response_model": response_model,
        }
        wrapper.core_func = func  # type: ignore
        return wrapper

    return decorator


class HttpController(Controller, metaclass=Singleton):
    """Base singleton class for HTTP API controllers using FastAPI.

    This class provides a foundation for creating RESTful API controllers with
    automatic route registration and OpenAPI documentation generation. It supports
    all standard HTTP methods (GET, POST, PUT, PATCH, DELETE) and handles route
    configuration, middleware, and response formatting.

    The controller automatically builds routes based on implemented methods that
    are decorated with the @router decorator. It integrates with FastAPI's
    dependency injection system and supports custom response classes, middleware,
    and route configurations.

    Attributes:
        prefix (str): URL prefix for all routes in this controller
        tags (list[str | Enum] | None): OpenAPI tags for documentation grouping
        dependencies (list[params.Depends] | None): FastAPI dependencies
        deprecated (bool | None): Whether the entire controller is deprecated
        response_class (type[Response] | None): Default response class
        route_class (type[APIRoute] | None): Custom route class for advanced configurations
        router (APIRouter): FastAPI router instance containing all routes

    Examples:
        class UserController(HttpController):
            prefix = '/users'
            tags = ['Users']

            @router('/users/{user_id}', status_code=200)
            async def get(self, user_id: int):
                return {'user_id': user_id}
    """

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
    """Base singleton class for command-line interface controllers.

    This class provides a foundation for creating CLI commands with automatic
    argument parsing using argparse. It handles command-line argument validation,
    parsing, and provides a structured way to implement CLI-based operations.

    The controller automatically sets up argument parsing based on the args
    attribute and provides a consistent interface for executing CLI commands
    through the run() and execute() methods.

    Attributes:
        args (list[str]): List of required command-line argument names
        data: Parsed command-line arguments accessible as attributes

    Examples:
        class CreateUserController(CliController):
            name = 'create-user'
            args = ['username', 'email']

            async def execute(self):
                username = self.data.username
                email = self.data.email
                # Implementation here
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
        """Execute the CLI command logic.

        This method must be implemented by subclasses to define the actual
        command behavior. It will be called by the run() method after
        argument parsing is complete.

        Raises:
            NotImplementedError: If not implemented by subclass
        """
        raise NotImplementedError()
