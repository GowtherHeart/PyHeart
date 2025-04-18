from datetime import datetime


class TasksTyping:
    type id = int
    type name = str
    type content = str | None
    type complete = bool
    type date_create = datetime
    type date_update = datetime
    type deleted = bool


class TasksCustomTyping:
    type name = TasksTyping.name | None
    type date_create = TasksTyping.date_create | None
    type complete = TasksTyping.complete | None
    type deleted = TasksTyping.deleted | None
