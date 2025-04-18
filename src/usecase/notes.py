from src.internal.transaction import transaction
from src.models.db.notes import NoteCoreModel
from src.models.request.notes import (
    NotesCreatePldModel,
    NotesDeletePrmModel,
    NotesGetPrmModel,
    NotesUpdatePldModel,
)
from src.pkg.abc.usecase import Usecase
from src.repository import notes as note_repo


class NotesV1US(Usecase):
    async def get(self, model: NotesGetPrmModel) -> list[NoteCoreModel]:
        return await note_repo.SelectQuery(
            name=model.name,
            date_create=model.date_create,
            limit=model.limit,
            offset=model.offset,
        ).execute()

    @transaction
    async def create(self, payload: NotesCreatePldModel) -> NoteCoreModel:
        return await note_repo.CreateQuery(
            name=payload.name,
            content=payload.content,
        ).execute()

    @transaction
    async def update(self, payload: NotesUpdatePldModel) -> list[NoteCoreModel]:
        return await note_repo.UpdateQuery(
            name=payload.name,
            content=payload.content,
        ).execute()

    async def delete(self, model: NotesDeletePrmModel) -> list[NoteCoreModel]:
        return await note_repo.UpdateQuery(
            name=model.name,
            deleted=True,
        ).execute()
