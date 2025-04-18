from ._base import App


class HttpApp(App):
    def __init__(self) -> None:
        from src import Mapper
        from src.config.app import Config

        cmd_obj = Mapper().MAP["Http"]
        Config(cmd_obj.config_array)  # type: ignore
        app = Mapper().MAP["Http"]()
        self._app = app

    @property
    def app(self):
        return self._app
