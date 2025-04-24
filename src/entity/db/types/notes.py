from datetime import datetime


class NotesTyping:
    """
    A class to represent the typing annotations for a Note entity.
    """

    type id = int
    type name = str
    type content = str | None
    type date_create = datetime
    type date_update = datetime
    type deleted = bool


class NotesCustomTyping:
    """
    A class to represent custom typing annotations for a Note entity.
    """

    type name = NotesTyping.name | None
    type date_create = NotesTyping.date_create | None
    type deleted = NotesTyping.deleted | None
