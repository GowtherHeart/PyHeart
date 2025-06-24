from pydantic import Field

from src.pkg.abc.entity import Entity, FieldEntity

from .types.tasks import TasksCustomTyping, TasksTyping


class TasksEntity(Entity):
    """Database entity representing tasks with all core fields."""

    class id(FieldEntity):
        id: TasksTyping.id = Field(...)

    class name(FieldEntity):
        name: TasksTyping.name = Field(...)

    class content(FieldEntity):
        content: TasksTyping.content = Field(...)

    class complete(FieldEntity):
        complete: TasksTyping.complete = Field(...)

    class date_create(FieldEntity):
        date_create: TasksTyping.date_create = Field(...)

    class date_update(FieldEntity):
        date_update: TasksTyping.date_update = Field(...)

    class deleted(FieldEntity):
        deleted: TasksTyping.deleted = Field(...)


class TasksCustomEntity(Entity):
    """Custom database entity for optional task fields and operations."""

    class name_op(FieldEntity):
        name: TasksCustomTyping.name = Field(None)

    class date_create_op(FieldEntity):
        date_create: TasksCustomTyping.date_create = Field(None)
