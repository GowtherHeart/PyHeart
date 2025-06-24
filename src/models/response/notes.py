from src.entity.db.notes import NotesEntity
from src.pkg.abc.model import ResponseModel

__all__ = ["NotesCoreRespModel"]


class NotesCoreRespModel(
    ResponseModel,
    NotesEntity.name,
    NotesEntity.content,
    NotesEntity.date_create,
    NotesEntity.date_update,
    NotesEntity.deleted,
):
    """Response model for notes."""
