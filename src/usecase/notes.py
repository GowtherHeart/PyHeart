from src.internal.exception import EmptyResultException
from src.internal.transaction import transaction
from src.models.db.notes import NoteCoreModel
from src.models.request import notes as note_req
from src.pkg.abc.usecase import Usecase
from src.repository import notes as note_repo


class NotesV1US(Usecase):
    async def get(self, model: note_req.GetPrmModel) -> list[NoteCoreModel]:
        return await note_repo.SelectQuery(
            name=model.name,
            date_create=model.date_create,
            limit=model.limit,
            offset=model.offset,
        ).execute()

    @transaction
    async def create(self, payload: note_req.CreatePldModel) -> NoteCoreModel:
        return await note_repo.CreateQuery(
            name=payload.name,
            content=payload.content,
        ).execute()

    @transaction
    async def update(self, payload: note_req.UpdatePldModel) -> NoteCoreModel:
        effect = await note_repo.UpdateQuery(
            name=payload.name,
            content=payload.content,
        ).execute()
        if len(effect) == 0:
            raise EmptyResultException()

        return effect[0]

    async def delete(self, model: note_req.DeletePrmModel) -> NoteCoreModel:
        effect = await note_repo.UpdateQuery(
            name=model.name,
            deleted=True,
        ).execute()
        if len(effect) == 0:
            raise EmptyResultException()

        return effect[0]
