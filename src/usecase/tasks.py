from src.internal.transaction import transaction
from src.models.db.tasks import TaskCoreModel
from src.models.request.tasks import (
    TasksCreatePldModel,
    TasksDeletePrmModel,
    TasksGetPrmModel,
    TasksUpdatePldModel,
)
from src.pkg.abc.usecase import Usecase
from src.repository import tasks as task_repo


class TasksV1US(Usecase):
    async def get(self, model: TasksGetPrmModel) -> list[TaskCoreModel]:
        return await task_repo.SelectQuery(
            name=model.name,
            date_create=model.date_create,
            limit=model.limit,
            offset=model.offset,
        ).execute()

    @transaction
    async def create(self, payload: TasksCreatePldModel) -> TaskCoreModel:
        return await task_repo.CreateQuery(
            name=payload.name,
            content=payload.content,
        ).execute()

    @transaction
    async def update(self, payload: TasksUpdatePldModel) -> list[TaskCoreModel]:
        return await task_repo.UpdateQuery(
            name=payload.name,
            content=payload.content,
        ).execute()

    async def delete(self, model: TasksDeletePrmModel) -> list[TaskCoreModel]:
        return await task_repo.UpdateQuery(
            name=model.name,
            deleted=True,
        ).execute()
