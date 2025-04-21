from src.pkg.core.exception import CoreException


class NoteCreateException(CoreException):
    status_code = 400
    detail = "can`t create notes"


class NoteUpdateException(CoreException):
    status_code = 400
    detail = "can`t update notes"
