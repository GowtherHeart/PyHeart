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
    """
    NotesCoreControllerV1 is responsible for handling HTTP requests related to notes.
    It provides endpoints for creating, retrieving, updating, and deleting notes.
    The controller uses NotesV1US use case to perform operations and returns responses
    in the form of NotesCoreResponseModel.
    """

    prefix = "/notes"
    tags = ["notes"]

    spec_route = ["post_test"]

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

    @router(
        path="/test",
        status_code=status.HTTP_200_OK,
    )
    async def post_test(self) -> str:
        return "TEST!"
