from src.entity.db.core import CoreEntity
from src.entity.db.notes import NotesCustomEntity, NotesEntity
from src.pkg.abc.model import ParamsModel, PayloadModel

__all__ = ["NotesCreatePldModel", "NotesUpdatePldModel", "NotesGetPrmModel"]


class NotesGetPrmModel(
    ParamsModel,
    NotesCustomEntity.name_op,
    NotesCustomEntity.date_create_op,
    CoreEntity.limit,
    CoreEntity.offset,
):
    """
    A model for retrieving parameters related to notes. This class extends the ParamsModel
    and includes operations for filtering by name and creation date, as defined in the
    NotesCustomEntity.
    """


class NotesDeletePrmModel(
    ParamsModel,
    NotesEntity.name,
):
    """
    A model for handling parameters required to delete notes. This class extends the ParamsModel
    and includes operations for specifying the name of the note to be deleted, as defined in the
    NotesEntity.
    """


class NotesCreatePldModel(
    PayloadModel,
    NotesEntity.name,
    NotesEntity.content,
):
    """
    A model for creating a new note. This class extends the PayloadModel and includes
    fields for the name and content of the note, as defined in the NotesEntity.
    """


class NotesUpdatePldModel(
    PayloadModel,
    NotesEntity.name,
    NotesEntity.content,
):
    """
    A model for updating an existing note. This class extends the PayloadModel and includes
    fields for the name and content of the note, as defined in the NotesEntity. It is used
    to specify the data required to update a note's details.
    """
