from src.internal.transaction import transaction
from src.models.db.internal import InternalPostgresCoreModel
from src.models.request.internal import (
    PgCreatePldModel,
    PgDeletePrmModel,
    PgPldModel,
    PgPrmModel,
)
from src.pkg.abc.usecase import Usecase
from src.repository import internal as internal_repo


async def mock_select():
    await internal_repo.SelectQuery(
        name="1",
        limit=1,
        offset=0,
    ).execute()


class InternalPgV1US(Usecase):
    async def get(self, model: PgPrmModel) -> list[InternalPostgresCoreModel]:
        return await internal_repo.SelectQuery(
            name=model.name,
            limit=model.limit,
            offset=model.offset,
        ).execute()

    async def create(self, payload: PgCreatePldModel) -> InternalPostgresCoreModel:
        return await internal_repo.CreateQuery(
            name=payload.name,
            value=payload.value,
        ).execute()

    async def update(self, payload: PgPldModel) -> InternalPostgresCoreModel:
        return await internal_repo.UpdateQuery(
            name=payload.name,
            value=payload.value,
        ).execute()

    async def delete(self, model: PgDeletePrmModel) -> InternalPostgresCoreModel:
        return await internal_repo.DeleteQuery(
            name=model.name,
        ).execute()

    @transaction
    async def create_tx(self, payload: PgCreatePldModel) -> InternalPostgresCoreModel:
        await mock_select()
        return await internal_repo.CreateQuery(
            name=payload.name,
            value=payload.value,
        ).execute()

    @transaction
    async def update_tx(self, payload: PgPldModel) -> InternalPostgresCoreModel:
        await mock_select()
        return await internal_repo.UpdateQuery(
            name=payload.name,
            value=payload.value,
        ).execute()

    @transaction
    async def delete_tx(self, model: PgDeletePrmModel) -> InternalPostgresCoreModel:
        await mock_select()
        return await internal_repo.DeleteQuery(
            name=model.name,
        ).execute()

    @transaction
    async def create_tx_exc(
        self, payload: PgCreatePldModel
    ) -> InternalPostgresCoreModel:
        await mock_select()
        effect = await internal_repo.CreateQuery(
            name=payload.name,
            value=payload.value,
        ).execute()
        raise ValueError("Error")
        return effect

    @transaction
    async def update_tx_exc(self, payload: PgPldModel) -> InternalPostgresCoreModel:
        await mock_select()
        effect = await internal_repo.UpdateQuery(
            name=payload.name,
            value=payload.value,
        ).execute()
        raise ValueError("Error")
        return effect

    @transaction
    async def delete_tx_exc(self, model: PgDeletePrmModel) -> InternalPostgresCoreModel:
        await mock_select()
        effect = await internal_repo.DeleteQuery(
            name=model.name,
        ).execute()
        raise ValueError("Error")
        return effect
