import uvicorn
from fastapi import APIRouter, FastAPI, Request
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from loguru import logger
from starlette.responses import JSONResponse

from src.config.app import ConfigName, get_config
from src.controllers.notes.http_v1 import NotesCoreControllerV1
from src.internal.redis import core_redis
from src.pkg.abc.cmd import Cmd
from src.pkg.core.exception import CoreException
from src.pkg.driver.postgres._main import PostgresDriver
from src.pkg.driver.query import inject as db_inject
from src.pkg.fastapi.middleware import MasterMiddelware
from src.repository import _startup as _startup_repo
from src.repository import notes as notes_repo

__all__ = ["HttpCmd"]


class HttpCmd(Cmd):
    """HTTP server command for running the FastAPI web application.

    This command initializes and runs the complete web server with all necessary
    components including database connections, Redis cache, middleware, controllers,
    and API documentation. It serves as the main entry point for the web application.

    The command sets up:
    - FastAPI application with custom OpenAPI documentation
    - Database connection pools (PostgreSQL)
    - Redis cache connections
    - HTTP middleware stack
    - API route registration for all controllers
    - Exception handlers
    - Startup initialization procedures

    Configuration Dependencies:
    - HTTP: Server host, port, worker configuration
    - POSTGRES: Database connection parameters
    - REDIS: Cache connection parameters
    - LOGGING: Application logging configuration

    Attributes:
        name (str): Command identifier "Http"
        config_array (list[str]): Required configuration sections
        _app (FastAPI): The FastAPI application instance

    Examples:
        # The command is typically run via the main application:
        # python main.py --cmd Http

        # Or programmatically:
        cmd = HttpCmd()
        cmd.run()
    """

    name = "Http"
    config_array = [
        ConfigName.HTTP,
        ConfigName.POSTGRES,
        ConfigName.REDIS,
        ConfigName.LOGGING,
    ]

    _app = FastAPI(
        swagger_ui_parameters={
            "defaultModelsExpandDepth": -1,
            "syntaxHighlight": {"theme": "tomorrow-night"},
        },
        docs_url=None,  # Disable default docs
        redoc_url=None,  # Disable redoc
    )

    def custom_openapi(self):
        if self._app.openapi_schema:
            return self._app.openapi_schema

        openapi_schema = get_openapi(
            title="PyHeart",
            version="1.0.0",
            description="",
            routes=self._app.routes,
        )

        self._app.openapi_schema = openapi_schema
        return self._app.openapi_schema

    def __init__(self) -> None:
        self._config = get_config()
        self._app.add_middleware(MasterMiddelware)
        self._init_repo()
        self.__reg_controller_v1()
        setattr(self._app, "openapi", self.custom_openapi)

    def _init_repo(self) -> None:
        driver = PostgresDriver(
            host=get_config().POSTGRES.HOST,
            port=get_config().POSTGRES.PORT,
            username=get_config().POSTGRES.USERNAME,
            password=get_config().POSTGRES.PASSWORD,
            db=get_config().POSTGRES.DB,
        )
        db_inject(_startup_repo, driver)
        db_inject(notes_repo, driver)

    def __reg_controller_v1(self) -> None:
        router_v1 = APIRouter(prefix="/v1")

        notes_controller = NotesCoreControllerV1()
        router_v1.include_router(router=notes_controller.router)

        self._app.include_router(router=router_v1)

        # Add custom dark theme docs endpoint
        @self._app.get("/docs", include_in_schema=False)
        async def custom_swagger_ui_html():
            return get_swagger_ui_html(
                openapi_url="/openapi.json",
                title="PyHeart - Swagger UI",
                swagger_ui_parameters={
                    "defaultModelsExpandDepth": -1,
                    "syntaxHighlight": {"theme": "tomorrow-night"},
                    "tryItOutEnabled": True,
                    "docExpansion": "none",
                    "displayRequestDuration": True,
                    "filter": True,
                },
            )

    @staticmethod
    @_app.exception_handler(CoreException)
    async def validation_exception_handler(
        request: Request, exc: CoreException
    ) -> JSONResponse:
        _ = request
        return JSONResponse(
            {
                "exception": {
                    "message": exc.detail,
                },
                "status_code": exc.status_code,
                "payload": None,
            },
            status_code=exc.status_code,
        )

    @staticmethod
    @_app.on_event("startup")
    async def starup():
        with logger.contextualize(request_id="init"):
            await _startup_repo.InitConnectionQuery().execute()
            await core_redis().get("first")
        return

    def __call__(self) -> FastAPI:
        return self._app

    def run(self) -> None:
        uvicorn.run(
            "main:app",
            host=self._config.HTTP.HOST,
            port=self._config.HTTP.PORT,
            workers=self._config.HTTP.WORKER,
            factory=True,
            reload=self._config.HTTP.RELOAD,
            log_config=None,
        )
