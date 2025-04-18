import hashlib
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional

import redis.asyncio as aioredis

__all__ = ["RedisDriver"]


class _Singleton(type):
    _inst_map: dict = {}

    def _merge_param(cls, *args, **kwargs) -> str:
        result = []
        for v in args:
            result.append(str(v))
        for _, v in kwargs.items():
            result.append(str(v))

        m = hashlib.sha256()
        m.update("".join(result).encode("utf-8"))
        return m.hexdigest()

    def __call__(cls, *args, **kwargs):
        param_hex = cls._merge_param(*args, **kwargs)
        if param_hex not in cls._inst_map:
            cls._inst_map[param_hex] = super(_Singleton, cls).__call__(*args, **kwargs)

        return cls._inst_map[param_hex]


class RedisDriver(metaclass=_Singleton):

    _connector: Optional[aioredis.Redis] = None

    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
        db: str,
        max_connection: int = 10,
    ) -> None:
        self.__host = host
        self.__port = port
        self.__username = username
        self.__password = password
        self.__db = db
        self.pool = aioredis.ConnectionPool.from_url(
            self.__create_dsn(), max_connections=max_connection
        )

    def __create_dsn(self) -> str:
        return (
            f"redis://{self.__username}:{self.__password}"
            + f"@{self.__host}:{self.__port}/{self.__db}"
        )

    @asynccontextmanager
    async def _create_connector(self) -> AsyncGenerator[aioredis.Redis, None]:
        if self._connector is None:
            self._connector = aioredis.Redis(connection_pool=self.pool)

        try:
            yield self._connector
        finally:
            await self._connector.close()

    async def set(self, name: str, value: str, expire: Optional[int] = None) -> None:
        async with self._create_connector() as redis:
            async with redis.client() as conn:
                await conn.set(name=name, value=value, ex=expire)

    async def get(self, name: str) -> str:
        async with self._create_connector() as redis:
            async with redis.client() as conn:
                return await conn.get(name=name)

    async def delete(self, name: str) -> None:
        async with self._create_connector() as redis:
            async with redis.client() as conn:
                await conn.delete(name)
