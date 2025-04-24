__all__ = ["Cmd", "Mapper"]


class Cmd:
    """
    The Cmd class serves as an abstract base class for command implementations.
    It defines the structure and expected behavior for any command, including
    a name and a configuration array. Subclasses should implement the `run` method
    to define specific command actions.
    """

    name: str = NotImplemented
    config_array: list[str] = NotImplemented

    def run(self) -> None:
        raise NotImplementedError()


class Mapper:
    """
    The Mapper class is responsible for maintaining a mapping between command names
    and their corresponding command classes. This allows for dynamic retrieval and
    execution of commands based on their names. The MAP attribute should be a dictionary
    where keys are command names (strings) and values are command classes (subclasses of Cmd).
    """

    MAP: dict[str, type[Cmd]] = NotImplemented
