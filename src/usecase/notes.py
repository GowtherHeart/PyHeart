from src.internal.exception import EmptyResultException
from src.internal.transaction import transaction
from src.models.db.notes import NoteCoreModel
from src.models.request import notes as note_req
from src.pkg.abc.usecase import Usecase
from src.repository import notes as note_repo


class NotesV1US(Usecase):
    """Use case class for notes business logic operations (version 1)."""

    async def get(self, model: note_req.GetPrmModel) -> list[NoteCoreModel]:
        """Retrieve notes with optional filtering and pagination."""
        return await note_repo.SelectQuery(
            name=model.name,
            date_create=model.date_create,
            limit=model.limit,
            offset=model.offset,
        ).execute()

    @transaction
    async def create(self, payload: note_req.CreatePldModel) -> NoteCoreModel:
        """Create a new note with transaction management.

        Args:
            payload (note_req.CreatePldModel): Note creation data containing
                                             name and content

        Returns:
            NoteCoreModel: The created note with generated ID and timestamps

        Raises:
            NoteCreateException: If note creation fails due to validation or
                               database constraints

        Examples:
            note = await usecase.create(CreatePldModel(
                name="My New Note",
                content="This is the note content"
            ))
        """
        return await note_repo.CreateQuery(
            name=payload.name,
            content=payload.content,
        ).execute()

    @transaction
    async def update(self, payload: note_req.UpdatePldModel) -> NoteCoreModel:
        """Update an existing note with transaction management.

        Args:
            payload (note_req.UpdatePldModel): Note update data containing
                                             name and content

        Returns:
            NoteCoreModel: The updated note with new values and updated timestamp

        Raises:
            EmptyResultException: If no note was found to update
            NoteUpdateException: If note update fails due to validation or
                               database constraints

        Examples:
            updated_note = await usecase.update(UpdatePldModel(
                name="Updated Note Title",
                content="Updated note content"
            ))
        """
        effect = await note_repo.UpdateQuery(
            name=payload.name,
            content=payload.content,
        ).execute()
        if len(effect) == 0:
            raise EmptyResultException()

        return effect[0]

    async def delete(self, model: note_req.DeletePrmModel) -> NoteCoreModel:
        """Soft delete a note by marking it as deleted.

        This method performs a soft delete by setting the deleted flag to True
        rather than physically removing the note from the database.

        Args:
            model (note_req.DeletePrmModel): Delete parameters containing the
                                           note identifier (name)

        Returns:
            NoteCoreModel: The deleted note with updated deleted flag

        Raises:
            EmptyResultException: If no note was found to delete

        Examples:
            deleted_note = await usecase.delete(DeletePrmModel(
                name="Note to Delete"
            ))
        """
        effect = await note_repo.UpdateQuery(
            name=model.name,
            deleted=True,
        ).execute()
        if len(effect) == 0:
            raise EmptyResultException()

        return effect[0]
