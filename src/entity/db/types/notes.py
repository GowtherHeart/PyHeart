from datetime import datetime


class NotesTyping:
    """Type annotations for Note entity fields."""

    type id = int
    type name = str
    type content = str | None
    type date_create = datetime
    type date_update = datetime
    type deleted = bool


class NotesCustomTyping:
    """Custom type annotations for optional Note entity fields."""

    type name = NotesTyping.name | None
    type date_create = NotesTyping.date_create | None
    type deleted = NotesTyping.deleted | None
