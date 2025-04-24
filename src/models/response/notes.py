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
    """A response model for notes that includes fields from both the ResponseModel and NotesEntity.

    This model aggregates various attributes from the NotesEntity such as name, content, date of creation,
    date of update, and deletion status, providing a comprehensive response structure for note-related operations.
    """
