from src.pkg.abc.controller import HttpController as _HttpController

from .response import MasterResponse
from .route import MasterRoute


class HttpController(_HttpController):
    response_class = MasterResponse
    route_class = MasterRoute
