class Singleton(type):
    """Metaclass for implementing the Singleton design pattern."""

    _map: dict = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._map:
            cls._map[cls] = super().__call__(*args, **kwargs)

        return cls._map[cls]


class Usecase(metaclass=Singleton):
    """Base singleton class for implementing business logic use cases."""
