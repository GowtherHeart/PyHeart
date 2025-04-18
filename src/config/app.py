import argparse
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigName:
    HTTP = "HTTP"
    POSTGRES = "POSTGRES"
    CLI = "CLI"
    REDIS = "REDIS"


class HttpSettings(BaseSettings):
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
    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        env_file_encoding="utf-8",
        env_prefix="CLI__",
        extra="ignore",
    )

    DEBUG: str = Field(validate_default=False)


class PostgresSettings(BaseSettings):
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


MAP = {
    ConfigName.POSTGRES: PostgresSettings,
    ConfigName.HTTP: HttpSettings,
    ConfigName.CLI: CliSettings,
    ConfigName.REDIS: RedisSettings,
}


class Singleton(type):
    _map: dict = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._map:
            cls._map[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._map[cls]


class Config(metaclass=Singleton):
    HTTP: HttpSettings
    CLI: CliSettings
    POSTGRES: PostgresSettings
    REDIS: RedisSettings

    CMD: str | None = None
    TESTING: bool = False

    def __init__(self, settings: list) -> None:
        for el in settings:
            var = MAP.get(el, None)
            if var is None:
                continue

            setattr(self, el, var())


def arg_parser() -> argparse.Namespace:
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
    return Config()  # type: ignore
