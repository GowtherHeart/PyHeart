from starlette import status

from src.entity.db.types.core import CoreTyping
from src.entity.db.types.tasks import TasksCustomTyping, TasksTyping
from src.internal.fastapi.controller import HttpController
from src.models.request import tasks as task_req
from src.models.response.tasks import TasksCoreRespModel
from src.pkg.abc.controller import router
from src.usecase.tasks import TasksV1US


class TasksCoreControllerV1(HttpController):
    """HTTP API controller for task management (version 1)."""

    prefix = "/tasks"
    tags = ["tasks"]

    @router(path="/", status_code=status.HTTP_200_OK)
    async def get(
        self,
        name: TasksCustomTyping.name = None,
        date_create: TasksCustomTyping.date_create = None,
        limit: CoreTyping.limit = 100,
        offset: CoreTyping.offset = 0,
    ) -> list[TasksCoreRespModel]:
        """Retrieve tasks with optional filtering and pagination."""
        model = task_req.GetPrmModel(
            name=name,
            date_create=date_create,
            limit=limit,
            offset=offset,
        )
        result = await TasksV1US().get(model=model)
        return [TasksCoreRespModel(**e.model_dump()) for e in result]

    @router(path="/", status_code=status.HTTP_201_CREATED)
    async def post(self, payload: task_req.CreatePldModel) -> TasksCoreRespModel:
        """Create a new task."""
        result = await TasksV1US().create(payload=payload)
        return TasksCoreRespModel(**result.model_dump())

    @router(path="/", status_code=status.HTTP_200_OK)
    async def patch(self, payload: task_req.UpdatePldModel) -> TasksCoreRespModel:
        """Update an existing task by name."""
        result = await TasksV1US().update(payload=payload)
        return TasksCoreRespModel(**result.model_dump())

    @router(path="/", status_code=status.HTTP_200_OK)
    async def delete(self, name: TasksTyping.name) -> TasksCoreRespModel:
        """Soft delete a task by name."""
        model = task_req.DeletePrmModel(name=name)
        result = await TasksV1US().delete(model=model)
        return TasksCoreRespModel(**result.model_dump())
