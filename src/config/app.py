import argparse
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigName:
    """Configuration section name constants.

    This class defines string constants for different configuration sections
    used throughout the application. These constants ensure consistent naming
    and help prevent typos when referencing configuration sections.

    Attributes:
        HTTP (str): HTTP server configuration section name
        POSTGRES (str): PostgreSQL database configuration section name
        CLI (str): Command-line interface configuration section name
        REDIS (str): Redis cache configuration section name
        LOGGING (str): Logging system configuration section name
    """

    HTTP = "HTTP"
    POSTGRES = "POSTGRES"
    CLI = "CLI"
    REDIS = "REDIS"
    LOGGING = "LOGGING"


class HttpSettings(BaseSettings):
    """HTTP server configuration settings.

    This class defines configuration options for the HTTP server including
    connection parameters, worker processes, and development settings.
    Settings are automatically loaded from environment variables with the
    'HTTP__' prefix.

    Attributes:
        HOST (str): Server host address to bind to
        PORT (int): Server port number to listen on
        WORKER (int): Number of worker processes for handling requests
        RELOAD (bool): Enable auto-reload for development mode

    Environment Variables:
        HTTP__HOST: Server host (e.g., '0.0.0.0', 'localhost')
        HTTP__PORT: Server port (e.g., 8000, 3000)
        HTTP__WORKER: Worker count (e.g., 1, 4)
        HTTP__RELOAD: Auto-reload flag (e.g., true, false)
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        env_file_encoding="utf-8",
        env_prefix="HTTP__",
        extra="ignore",
    )

    HOST: str = Field(validate_default=False)
    PORT: int = Field(validate_default=False)
    WORKER: int = Field(validate_default=False)
    RELOAD: bool = Field(validate_default=False)


class CliSettings(BaseSettings):
    """Command-line interface configuration settings.

    This class defines configuration options for CLI operations and debugging.
    Settings are automatically loaded from environment variables with the
    'CLI__' prefix.

    Attributes:
        DEBUG (str): Debug mode configuration for CLI operations

    Environment Variables:
        CLI__DEBUG: Debug level or mode (e.g., 'true', 'verbose', 'off')
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        env_file_encoding="utf-8",
        env_prefix="CLI__",
        extra="ignore",
    )

    DEBUG: str = Field(validate_default=False)


class PostgresSettings(BaseSettings):
    """PostgreSQL database configuration settings.

    This class defines connection parameters for PostgreSQL database access.
    Settings are automatically loaded from environment variables with the
    'PG__' prefix for security and flexibility.

    Attributes:
        HOST (str): Database server hostname or IP address
        PORT (int): Database server port number
        USERNAME (str): Database connection username
        PASSWORD (str): Database connection password
        DB (str): Database name to connect to

    Environment Variables:
        PG__HOST: Database host (e.g., 'localhost', 'db.example.com')
        PG__PORT: Database port (e.g., 5432)
        PG__USERNAME: Database username
        PG__PASSWORD: Database password
        PG__DB: Database name
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        env_file_encoding="utf-8",
        env_prefix="PG__",
        extra="ignore",
    )

    HOST: str = Field(validate_default=False)
    PORT: int = Field(validate_default=False)
    USERNAME: str = Field(validate_default=False)
    PASSWORD: str = Field(validate_default=False)
    DB: str = Field(validate_default=False)


class RedisSettings(BaseSettings):
    """Redis cache configuration settings.

    This class defines connection parameters for Redis cache access including
    authentication and database selection. Settings are automatically loaded
    from environment variables with the 'REDIS__' prefix.

    Attributes:
        HOST (str): Redis server hostname or IP address
        PORT (int): Redis server port number
        USERNAME (str): Redis connection username (Redis 6+)
        PASSWORD (str): Redis connection password
        DB (str): Redis database number to select

    Environment Variables:
        REDIS__HOST: Redis host (e.g., 'localhost', 'redis.example.com')
        REDIS__PORT: Redis port (e.g., 6379)
        REDIS__USERNAME: Redis username (optional)
        REDIS__PASSWORD: Redis password (optional)
        REDIS__DB: Redis database number (e.g., '0', '1')
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        env_file_encoding="utf-8",
        env_prefix="REDIS__",
        extra="ignore",
    )

    HOST: str = Field(validate_default=False)
    PORT: int = Field(validate_default=False)
    USERNAME: str = Field(validate_default=False)
    PASSWORD: str = Field(validate_default=False)
    DB: str = Field(validate_default=False)


class LoggingSettings(BaseSettings):
    """Logging system configuration settings.

    This class defines configuration options for the application's logging
    system including log levels and output formatting. Settings are loaded
    from environment variables with the 'LOGGING__' prefix.

    Attributes:
        LVL (str): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    Environment Variables:
        LOGGING__LVL: Log level (e.g., 'DEBUG', 'INFO', 'ERROR')
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        env_file_encoding="utf-8",
        env_prefix="LOGGING__",
        extra="ignore",
    )

    LVL: str = Field(validate_default=False)


MAP = {
    ConfigName.POSTGRES: PostgresSettings,
    ConfigName.HTTP: HttpSettings,
    ConfigName.CLI: CliSettings,
    ConfigName.REDIS: RedisSettings,
    ConfigName.LOGGING: LoggingSettings,
}


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


class Config(metaclass=Singleton):
    """Main singleton configuration manager for the application.

    This class serves as the central configuration hub, managing all application
    settings including database connections, HTTP server parameters, Redis cache
    settings, CLI options, and logging configuration.

    The configuration is loaded dynamically based on the required settings list
    provided during initialization. Each setting section is instantiated only
    when needed, allowing for flexible configuration management.

    Attributes:
        HTTP (HttpSettings): HTTP server configuration
        CLI (CliSettings): CLI configuration
        POSTGRES (PostgresSettings): PostgreSQL database configuration
        REDIS (RedisSettings): Redis cache configuration
        LOGGING (LoggingSettings): Logging system configuration
        CMD (str | None): Current command being executed
        TESTING (bool): Flag indicating if running in test mode

    Examples:
        # Initialize with specific configuration sections
        config = Config(['HTTP', 'POSTGRES', 'LOGGING'])

        # Access configuration values
        db_host = config.POSTGRES.HOST
        server_port = config.HTTP.PORT
    """

    HTTP: HttpSettings
    CLI: CliSettings
    POSTGRES: PostgresSettings
    REDIS: RedisSettings
    LOGGING: LoggingSettings

    CMD: str | None = None
    TESTING: bool = False

    def __init__(self, settings: list) -> None:
        for el in settings:
            var = MAP.get(el, None)
            if var is None:
                continue

            setattr(self, el, var())


def arg_parser() -> argparse.Namespace:
    """Parse command-line arguments for application startup.

    This function creates and configures an argument parser for handling
    command-line options when starting the application. It supports command
    selection and additional arguments.

    Returns:
        argparse.Namespace: Parsed command-line arguments containing:
            - cmd: Selected command to execute ('Http', 'CreateNoteCli')
            - Additional unnamed arguments

    Examples:
        args = arg_parser()
        if args.cmd == 'Http':
            start_http_server()
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--cmd",
        "-c",
        choices=["Http", "CreateNoteCli"],
        default="Http",
        required=False,
    )
    parser.add_argument("*", nargs="*")
    args, _ = parser.parse_known_args()
    return args


@lru_cache()
def get_config() -> Config:
    """Get the singleton configuration instance with caching.

    This function returns the main application configuration instance,
    using LRU cache to ensure the same instance is returned on subsequent
    calls. The configuration is initialized without specific settings,
    allowing dynamic loading as needed.

    Returns:
        Config: The singleton configuration instance

    Examples:
        config = get_config()
        db_settings = config.POSTGRES
    """
    return Config()  # type: ignore
