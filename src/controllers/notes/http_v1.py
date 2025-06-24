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
    """HTTP API controller for notes management (version 1)."""

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
        """Retrieve a list of notes with optional filtering and pagination."""
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
        """Create a new note with the provided data."""
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
        """Update an existing note by name."""
        result = await NotesV1US().update(payload=payload)
        return NotesCoreRespModel(**result.model_dump())

    @router(
        path="/",
        status_code=status.HTTP_200_OK,
        responses={**EmptyResultException.generate_openapi()},
        response_model=NoteCoreResponseModelExample,
    )
    async def delete(self, name: NotesTyping.name) -> NotesCoreRespModel:
        """Soft delete a note by name."""
        model = note_req.DeletePrmModel(name=name)
        result = await NotesV1US().delete(model=model)
        return NotesCoreRespModel(**result.model_dump())
