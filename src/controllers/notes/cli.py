from loguru import logger

from src.models.request.notes import NotesCreatePldModel
from src.pkg.abc.controller import CliController
from src.usecase.notes import NotesV1US


class CreateNoteController(CliController):
    args = ["name", "content"]

    async def execute(self) -> None:
        payload = NotesCreatePldModel(
            content=self.data.content,
            name=self.data.name,
        )
        result = await NotesV1US().create(payload=payload)
        logger.info(result)
