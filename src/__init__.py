import os

from src.cmd import Mapper
from src.config.app import Config, arg_parser, get_config
from src.pkg.logging._main import LoggingInit

testing = bool(os.getenv("TESTING", False))
if testing is True:
    ...
else:
    arg_map = arg_parser()
    cmd_arg = arg_map.cmd

    if cmd_arg not in Mapper.MAP:
        raise ValueError()

    cmd_obj = Mapper().MAP[cmd_arg]
    Config(cmd_obj.config_array)  # type: ignore

    app = Mapper().MAP[cmd_arg]()

    LoggingInit(lvl=get_config().LOGGING.LVL)
