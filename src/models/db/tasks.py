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
    """
    TaskCoreModel is a database model that represents the core attributes of a task.
    It inherits from DbModel and includes fields from TasksEntity such as id, name,
    content, complete status, creation date, update date, and deletion status.
    """
