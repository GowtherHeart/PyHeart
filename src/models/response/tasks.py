from src.entity.db.tasks import TasksEntity
from src.pkg.abc.model import ResponseModel

__all__ = ["TasksCoreRespModel"]


class TasksCoreRespModel(
    ResponseModel,
    TasksEntity.name,
    TasksEntity.content,
    TasksEntity.complete,
    TasksEntity.date_create,
    TasksEntity.date_update,
    TasksEntity.deleted,
):
    """Response model for tasks."""
