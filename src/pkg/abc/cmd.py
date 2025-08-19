__all__ = ["Cmd", "Mapper"]


class Cmd:
    """Abstract base class for command implementations."""

    name: str = NotImplemented
    config_array: list[str] = NotImplemented

    def run(self) -> None:
        """Execute the command's main functionality."""
        raise NotImplementedError


class Mapper:
    """Command registry and dispatcher for dynamic command execution."""

    MAP: dict[str, type[Cmd]] = NotImplemented
