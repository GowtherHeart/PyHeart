from src.cmd.cli.note import CreateNoteCmd
from src.cmd.http import HttpCmd
from src.pkg.abc.cmd import Mapper as _Mapper


class Mapper(_Mapper):
    MAP = {HttpCmd.name: HttpCmd, CreateNoteCmd.name: CreateNoteCmd}
