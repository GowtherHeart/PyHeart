from src.entity.db.core import CoreEntity
from src.entity.db.notes import NotesCustomEntity, NotesEntity
from src.pkg.abc.model import ParamsModel, PayloadModel

__all__ = ["CreatePldModel", "GetPrmModel", "UpdatePldModel"]


class GetPrmModel(
    ParamsModel,
    NotesCustomEntity.name_op,
    NotesCustomEntity.date_create_op,
    CoreEntity.limit,
    CoreEntity.offset,
):
    """Parameters model for retrieving notes with filters."""


class DeletePrmModel(
    ParamsModel,
    NotesEntity.name,
):
    """Parameters model for deleting notes."""


class CreatePldModel(
    PayloadModel,
    NotesEntity.name,
    NotesEntity.content,
):
    """Payload model for creating a new note."""


class UpdatePldModel(
    PayloadModel,
    NotesEntity.name,
    NotesEntity.content,
):
    """Payload model for updating an existing note."""
