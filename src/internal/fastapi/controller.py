from src.pkg.abc.controller import HttpController as _HttpController

from .response import MasterResponse
from .route import MasterRoute


class HttpController(_HttpController):
    """
    HttpController is a subclass of _HttpController that specifies the response and route classes
    to be used within the application. It utilizes MasterResponse for handling HTTP responses and
    MasterRoute for managing routing logic.

    MasterResponse is responsible for formatting and sending HTTP responses back to the client.
    It ensures that the response structure adheres to the application's standards and may include
    additional functionalities such as logging or error handling.

    MasterRoute manages the routing logic within the application. It defines how incoming HTTP
    requests are mapped to the appropriate controller actions, ensuring that each request is
    processed by the correct handler based on the defined routes.
    """

    response_class = MasterResponse
    route_class = MasterRoute
