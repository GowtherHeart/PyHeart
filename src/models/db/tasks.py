from src.entity.db.tasks import TasksEntity
from src.pkg.abc.model import DbModel

__all__ = ["TaskCoreModel"]


class TaskCoreModel(
    DbModel,
    TasksEntity.id,
    TasksEntity.name,
    TasksEntity.content,
    TasksEntity.complete,
    TasksEntity.date_create,
    TasksEntity.date_update,
    TasksEntity.deleted,
):
    """Core database model for tasks."""
