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
        """
        Retrieve a list of notes based on the provided filters.

        Parameters:
        - name: Optional; filter notes by name.
        - date_create: Optional; filter notes by creation date.

        Returns:
        A list of NotesCoreResponseModel instances matching the filters.
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
        """
        Create a new note with the provided payload.

        Parameters:
        - payload: The data required to create a new note, encapsulated in NotesCreatePayloadModel.

        Returns:
        A NotesCoreResponseModel instance representing the newly created note.
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
        """
        Update an existing note with the provided payload.

        Parameters:
        - payload: The data required to update an existing note, encapsulated in NotesUpdatePayloadModel.

        Returns:
        A NotesCoreResponseModel instance representing the updated note.
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
        """
        Delete an existing note by its name.

        Parameters:
        - name: The name of the note to be deleted.

        Returns:
        A NotesCoreResponseModel instance representing the deleted note.
        """
        model = note_req.DeletePrmModel(name=name)
        result = await NotesV1US().delete(model=model)
        return NotesCoreRespModel(**result.model_dump())
