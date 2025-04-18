from src.entity.db.notes import NotesEntity
from src.pkg.abc.model import DbModel

__all__ = ["NoteCoreModel"]


class NoteCoreModel(
    DbModel,
    NotesEntity.id,
    NotesEntity.name,
    NotesEntity.content,
    NotesEntity.date_create,
    NotesEntity.date_update,
    NotesEntity.deleted,
):
    """A core model for notes that integrates database model functionalities with note-specific attributes."""
