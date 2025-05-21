__all__ = ["Cmd", "Mapper"]


class Cmd:
    """Abstract base class for command implementations.

    This class provides the foundation for all command-based operations in the
    application, including CLI commands and service commands. Each command has
    a unique name and configuration requirements that must be satisfied before
    execution.

    Commands are responsible for:
    - Defining their configuration dependencies
    - Implementing the core execution logic
    - Handling command-specific setup and teardown

    Attributes:
        name (str): Unique identifier for the command. Must be implemented by subclasses.
        config_array (list[str]): List of configuration sections required by this command.

    Examples:
        class HttpServerCmd(Cmd):
            name = 'http-server'
            config_array = ['HTTP', 'DATABASE', 'LOGGING']

            def run(self) -> None:
                # Start HTTP server implementation
                pass
    """

    name: str = NotImplemented
    config_array: list[str] = NotImplemented

    def run(self) -> None:
        """Execute the command's main functionality.

        This method must be implemented by subclasses to define the specific
        behavior of the command. It will be called after all configuration
        requirements have been validated and loaded.

        Raises:
            NotImplementedError: If not implemented by subclass
        """
        raise NotImplementedError()


class Mapper:
    """Command registry and dispatcher for dynamic command execution.

    This class maintains a registry of available commands and provides mechanisms
    for command discovery, registration, and execution. It enables dynamic command
    routing based on command names and supports command lifecycle management.

    The mapper is typically used by:
    - CLI applications for command dispatch
    - Service managers for operation routing
    - Plugin systems for command registration

    Attributes:
        MAP (dict[str, type[Cmd]]): Registry mapping command names to command classes.
                                   Must be implemented by subclasses.

    Examples:
        class ApplicationMapper(Mapper):
            MAP = {
                'serve': HttpServerCmd,
                'migrate': DatabaseMigrationCmd,
                'cli': CliInterfaceCmd
            }
    """

    MAP: dict[str, type[Cmd]] = NotImplemented
