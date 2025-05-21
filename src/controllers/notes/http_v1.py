from starlette import status

from src.entity.db.types.core import CoreTyping
from src.entity.db.types.notes import NotesCustomTyping, NotesTyping
from src.internal.exception import EmptyResultException, NoteCreateException
from src.internal.exception.notes import NoteUpdateException
from src.internal.fastapi.controller import HttpController
from src.models.request import notes as note_req
from src.models.response.notes import NotesCoreRespModel
from src.pkg.abc.controller import router
from src.usecase.notes import NotesV1US

from ._examples import NoteCoreResponseModelArrayExample, NoteCoreResponseModelExample


class NotesCoreControllerV1(HttpController):
    """HTTP API controller for notes management (version 1).

    This controller provides RESTful endpoints for complete notes management including
    creation, retrieval, updating, and deletion operations. It follows REST conventions
    and integrates with the NotesV1US use case for business logic execution.

    The controller handles:
    - GET /notes/ - Retrieve notes with optional filtering and pagination
    - POST /notes/ - Create new notes
    - PUT /notes/{id} - Update existing notes
    - DELETE /notes/{id} - Delete notes

    All endpoints return standardized responses using NotesCoreRespModel and handle
    appropriate HTTP status codes and error conditions.

    Attributes:
        prefix (str): URL prefix for all note endpoints ('/notes')
        tags (list[str]): OpenAPI tags for documentation grouping

    Examples:
        # The controller is automatically registered with FastAPI
        # Endpoints are available at:
        # GET /v1/notes/?limit=10&offset=0
        # POST /v1/notes/ with JSON payload
        # PUT /v1/notes/123 with JSON payload
        # DELETE /v1/notes/123
    """

    prefix = "/notes"
    tags = ["notes"]

    @router(
        path="/",
        status_code=status.HTTP_200_OK,
        response_model=NoteCoreResponseModelArrayExample,
    )
    async def get(
        self,
        name: NotesCustomTyping.name = None,
        date_create: NotesCustomTyping.date_create = None,
        limit: CoreTyping.limit = 100,
        offset: CoreTyping.offset = 0,
    ) -> list[NotesCoreRespModel]:
        """Retrieve a list of notes with optional filtering and pagination.

        This endpoint allows clients to retrieve notes from the database with support for:
        - Optional filtering by name (partial or exact match)
        - Optional filtering by creation date
        - Pagination with configurable limit and offset
        - Default limit of 100 items per request

        The endpoint returns a list of notes matching the specified criteria, sorted by
        creation date in descending order (newest first).

        Query Parameters:
            name (str, optional): Filter notes by name. Supports partial matching.
                                 Example: ?name=meeting will match "Meeting Notes"
            date_create (datetime, optional): Filter notes created on or after this date.
                                            Format: ISO 8601 (YYYY-MM-DDTHH:MM:SS)
            limit (int, optional): Maximum number of notes to return. Default: 100, Max: 1000
            offset (int, optional): Number of notes to skip for pagination. Default: 0

        Returns:
            list[NotesCoreRespModel]: Array of note objects containing:
                - name: The note's title/name
                - content: The note's text content
                - date_create: When the note was created (ISO 8601 format)
                - date_update: When the note was last updated (ISO 8601 format)
                - deleted: Boolean indicating if the note is soft-deleted

        Example Requests:
            GET /v1/notes/                           # Get all notes (first 100)
            GET /v1/notes/?limit=10&offset=20        # Get 10 notes starting from 21st
            GET /v1/notes/?name=meeting              # Get notes with 'meeting' in name
            GET /v1/notes/?date_create=2024-01-01    # Get notes created after Jan 1, 2024

        Example Response:
            [
                {
                    "name": "Meeting Notes",
                    "content": "Discussion points from today's meeting...",
                    "date_create": "2024-01-15T10:30:00Z",
                    "date_update": "2024-01-15T10:30:00Z",
                    "deleted": false
                },
                {
                    "name": "Project Ideas",
                    "content": "Brainstorming session results...",
                    "date_create": "2024-01-14T15:45:00Z",
                    "date_update": "2024-01-14T16:20:00Z",
                    "deleted": false
                }
            ]
        """
        model = note_req.GetPrmModel(
            name=name,
            date_create=date_create,
            limit=limit,
            offset=offset,
        )
        result = await NotesV1US().get(model=model)
        return [NotesCoreRespModel(**e.model_dump()) for e in result]

    @router(
        path="/",
        status_code=status.HTTP_201_CREATED,
        responses={
            **NoteCreateException.generate_openapi(),
            **EmptyResultException.generate_openapi(),
        },
        response_model=NoteCoreResponseModelExample,
    )
    async def post(self, payload: note_req.CreatePldModel) -> NotesCoreRespModel:
        """Create a new note with the provided data.

        This endpoint creates a new note in the database with the specified name and content.
        The note will be automatically assigned:
        - A unique identifier
        - Creation timestamp (current time)
        - Update timestamp (same as creation time)
        - Deleted status (false by default)

        The operation is performed within a database transaction to ensure consistency.

        Request Body (JSON):
            name (str, required): The title/name of the note.
                                 Must be between 1-255 characters.
                                 Example: "Meeting Notes"
            content (str, required): The main text content of the note.
                                   Can contain multiple lines and special characters.
                                   Example: "Discussion points from today's meeting..."

        Returns:
            NotesCoreRespModel: The created note object containing:
                - name: The note's title/name
                - content: The note's text content
                - date_create: When the note was created (ISO 8601 format)
                - date_update: When the note was created (same as date_create)
                - deleted: Always false for new notes

        Status Codes:
            201: Note created successfully
            400: Invalid request data (missing required fields, validation errors)
            500: Internal server error during creation

        Error Responses:
            - NoteCreateException: When note creation fails due to business logic constraints
            - EmptyResultException: When the creation operation returns no result

        Example Request:
            POST /v1/notes/
            Content-Type: application/json

            {
                "name": "Project Planning",
                "content": "Initial project planning session notes. Key decisions made..."
            }

        Example Response (201):
            {
                "name": "Project Planning",
                "content": "Initial project planning session notes. Key decisions made...",
                "date_create": "2024-01-15T14:30:00Z",
                "date_update": "2024-01-15T14:30:00Z",
                "deleted": false
            }
        """
        result = await NotesV1US().create(payload=payload)
        return NotesCoreRespModel(**result.model_dump())

    @router(
        path="/",
        status_code=status.HTTP_200_OK,
        responses={
            **NoteUpdateException.generate_openapi(),
            **EmptyResultException.generate_openapi(),
        },
        response_model=NoteCoreResponseModelExample,
    )
    async def patch(self, payload: note_req.UpdatePldModel) -> NotesCoreRespModel:
        """Update an existing note with new data.

        This endpoint updates an existing note by matching the provided name and updating
        its content. The update operation:
        - Finds the note by exact name match
        - Updates the content field
        - Sets the update timestamp to current time
        - Preserves the original creation timestamp
        - Maintains the current deleted status

        The operation is performed within a database transaction to ensure consistency.

        Request Body (JSON):
            name (str, required): The exact name of the note to update.
                                 Must match an existing note's name exactly.
                                 Example: "Meeting Notes"
            content (str, required): The new content to replace the existing content.
                                   Can contain multiple lines and special characters.
                                   Example: "Updated meeting notes with action items..."

        Returns:
            NotesCoreRespModel: The updated note object containing:
                - name: The note's title/name (unchanged)
                - content: The note's updated text content
                - date_create: Original creation timestamp (unchanged)
                - date_update: When the note was updated (current timestamp)
                - deleted: Current deletion status (unchanged)

        Status Codes:
            200: Note updated successfully
            400: Invalid request data (missing required fields, validation errors)
            404: Note not found (no note with matching name)
            500: Internal server error during update

        Error Responses:
            - NoteUpdateException: When note update fails due to business logic constraints
            - EmptyResultException: When no note is found with the specified name

        Example Request:
            PATCH /v1/notes/
            Content-Type: application/json

            {
                "name": "Project Planning",
                "content": "Updated project planning notes with new requirements and timeline."
            }

        Example Response (200):
            {
                "name": "Project Planning",
                "content": "Updated project planning notes with new requirements and timeline.",
                "date_create": "2024-01-15T14:30:00Z",
                "date_update": "2024-01-15T16:45:00Z",
                "deleted": false
            }
        """
        result = await NotesV1US().update(payload=payload)
        return NotesCoreRespModel(**result.model_dump())

    @router(
        path="/",
        status_code=status.HTTP_200_OK,
        responses={**EmptyResultException.generate_openapi()},
        response_model=NoteCoreResponseModelExample,
    )
    async def delete(self, name: NotesTyping.name) -> NotesCoreRespModel:
        """Soft delete a note by marking it as deleted.

        This endpoint performs a soft delete operation on a note, which means:
        - The note is not physically removed from the database
        - The 'deleted' flag is set to true
        - The note remains accessible for audit purposes
        - The note will be filtered out from normal retrieval operations
        - The update timestamp is set to the current time

        The operation finds the note by exact name match and marks it as deleted.

        Query Parameters:
            name (str, required): The exact name of the note to delete.
                                 Must match an existing note's name exactly.
                                 Example: ?name=Meeting Notes

        Returns:
            NotesCoreRespModel: The deleted note object containing:
                - name: The note's title/name (unchanged)
                - content: The note's text content (unchanged)
                - date_create: Original creation timestamp (unchanged)
                - date_update: When the note was deleted (current timestamp)
                - deleted: Set to true to indicate deletion

        Status Codes:
            200: Note deleted successfully
            400: Invalid request data (missing or invalid name parameter)
            404: Note not found (no note with matching name)
            500: Internal server error during deletion

        Error Responses:
            - EmptyResultException: When no note is found with the specified name

        Example Request:
            DELETE /v1/notes/?name=Project Planning

        Example Response (200):
            {
                "name": "Project Planning",
                "content": "Project planning notes with requirements and timeline.",
                "date_create": "2024-01-15T14:30:00Z",
                "date_update": "2024-01-15T17:20:00Z",
                "deleted": true
            }

        Note:
            To permanently delete notes, use the internal administrative endpoints
            or database maintenance procedures. This endpoint only performs soft deletion
            to maintain data integrity and audit trails.
        """
        model = note_req.DeletePrmModel(name=name)
        result = await NotesV1US().delete(model=model)
        return NotesCoreRespModel(**result.model_dump())
