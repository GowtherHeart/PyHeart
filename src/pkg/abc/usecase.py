class Singleton(type):
    _map: dict = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._map:
            cls._map[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._map[cls]


class Usecase(metaclass=Singleton):
    """
    The Usecase class is a singleton that ensures only one instance of itself
    is created. It uses the Singleton metaclass to manage its instantiation.
    This class can be used to define business logic or operations that should
    be executed in a consistent and controlled manner across the application.
    """

    ...
