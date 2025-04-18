from starlette import status

from src.entity.db.types.core import CoreTyping
from src.entity.db.types.internal import (
    InternalPgCustomTyping,
    InternalPgTyping,
)
from src.models.request.internal import (
    PgCreatePldModel,
    PgDeletePrmModel,
    PgPldModel,
    PgPrmModel,
)
from src.models.response.internal import InternalPgCoreRespModel
from src.pkg.abc.controller import HttpController, router
from src.usecase.internal import InternalPgV1US


class InternalPostgresSimpleControllerV1(HttpController):

    prefix = "/v1/postgres/simple"
    tags = ["postgres"]

    @router(path="/", status_code=status.HTTP_200_OK)
    async def get(
        self,
        name: InternalPgCustomTyping.name = None,
        limit: CoreTyping.limit = 100,
        offset: CoreTyping.offset = 0,
    ) -> list[InternalPgCoreRespModel]:
        model = PgPrmModel(
            name=name,
            limit=limit,
            offset=offset,
        )
        result = await InternalPgV1US().get(model=model)
        return [InternalPgCoreRespModel(**e.model_dump()) for e in result]

    @router(path="/", status_code=status.HTTP_201_CREATED)
    async def post(self, payload: PgCreatePldModel) -> InternalPgCoreRespModel:
        result = await InternalPgV1US().create(payload=payload)
        return InternalPgCoreRespModel(**result.model_dump())

    @router(path="/", status_code=status.HTTP_200_OK)
    async def patch(self, payload: PgPldModel) -> InternalPgCoreRespModel:
        result = await InternalPgV1US().update(payload=payload)
        return InternalPgCoreRespModel(**result.model_dump())

    @router(path="/", status_code=status.HTTP_200_OK)
    async def delete(self, name: InternalPgTyping.name) -> InternalPgCoreRespModel:
        model = PgDeletePrmModel(
            name=name,
        )
        result = await InternalPgV1US().delete(model=model)
        return InternalPgCoreRespModel(**result.model_dump())


class InternalPostgresTransactionControllerV1(HttpController):

    prefix = "/v1/postgres/transaction"
    tags = ["postgres"]

    @router(path="/", status_code=status.HTTP_201_CREATED)
    async def post(self, payload: PgCreatePldModel) -> InternalPgCoreRespModel:
        result = await InternalPgV1US().create_tx(payload=payload)
        return InternalPgCoreRespModel(**result.model_dump())

    @router(path="/", status_code=status.HTTP_200_OK)
    async def patch(self, payload: PgPldModel) -> InternalPgCoreRespModel:
        result = await InternalPgV1US().update_tx(payload=payload)
        return InternalPgCoreRespModel(**result.model_dump())

    @router(path="/", status_code=status.HTTP_200_OK)
    async def delete(self, name: InternalPgTyping.name) -> InternalPgCoreRespModel:
        model = PgDeletePrmModel(
            name=name,
        )
        result = await InternalPgV1US().delete_tx(model=model)
        return InternalPgCoreRespModel(**result.model_dump())


class InternalPostgresTransactionExcControllerV1(HttpController):

    prefix = "/v1/postgres/transaction_exception"
    tags = ["postgres"]

    @router(path="/", status_code=status.HTTP_201_CREATED)
    async def post(self, payload: PgCreatePldModel) -> InternalPgCoreRespModel:
        result = await InternalPgV1US().create_tx_exc(payload=payload)
        return InternalPgCoreRespModel(**result.model_dump())

    @router(path="/", status_code=status.HTTP_200_OK)
    async def patch(self, payload: PgPldModel) -> InternalPgCoreRespModel:
        result = await InternalPgV1US().update_tx_exc(payload=payload)
        return InternalPgCoreRespModel(**result.model_dump())

    @router(path="/", status_code=status.HTTP_200_OK)
    async def delete(self, name: InternalPgTyping.name) -> InternalPgCoreRespModel:
        model = PgDeletePrmModel(
            name=name,
        )
        result = await InternalPgV1US().delete_tx_exc(model=model)
        return InternalPgCoreRespModel(**result.model_dump())
