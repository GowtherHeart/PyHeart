class Singleton(type):
    """Metaclass for implementing the Singleton design pattern.

    This metaclass ensures that only one instance of a class can exist at a time.
    When a class uses this metaclass, subsequent instantiation attempts will
    return the same instance that was created on first instantiation.

    Attributes:
        _map (dict): Internal mapping of classes to their singleton instances.
    """

    _map: dict = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._map:
            cls._map[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._map[cls]


class Usecase(metaclass=Singleton):
    """Base singleton class for implementing business logic use cases.

    This class serves as the foundation for all business logic operations in the
    application. It ensures that each use case is implemented as a singleton,
    providing consistent state management and preventing multiple instances of
    the same business logic from existing simultaneously.

    The class is designed to be subclassed by specific use case implementations
    that handle discrete business operations such as user management, data
    processing, or workflow coordination.

    Examples:
        class UserManagementUsecase(Usecase):
            def create_user(self, user_data):
                # Implementation here
                pass
    """

    ...
