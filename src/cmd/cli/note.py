import asyncio

from loguru import logger

from src.controllers.notes.cli import CreateNoteController

from ._base import BaseCliCmd


class CreateNoteCmd(BaseCliCmd):
    name = "CreateNoteCli"

    def run(self) -> None:
        with logger.contextualize(request_id=""):
            self._prepare()
            controller = CreateNoteController()
            asyncio.run(controller.run())
