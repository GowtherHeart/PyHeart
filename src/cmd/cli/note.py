import asyncio

from src.controllers.notes.cli import CreateNoteController

from ._base import BaseCliCmd


class CreateNoteCmd(BaseCliCmd):
    name = "CreateNoteCli"

    def run(self) -> None:
        self._prepare()
        controller = CreateNoteController()
        asyncio.run(controller.run())
