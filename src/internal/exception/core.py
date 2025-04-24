from src.pkg.core.exception import CoreException

__all__ = ["EmptyResultException"]


class EmptyResultException(CoreException):
    status_code = 200
    detail = "empty result."
