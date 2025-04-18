from src.config.app import ConfigName, get_config
from src.pkg.abc.cmd import Cmd
from src.pkg.context import make_tx_id
from src.pkg.driver.postgres._main import PostgresDriver
from src.pkg.driver.query import inject as db_inject
from src.repository import _startup as _startup_repo
from src.repository import notes as notes_repo


class BaseCliCmd(Cmd):
    config_array = [ConfigName.CLI, ConfigName.POSTGRES]

    def _prepare(self) -> None:
        make_tx_id()

        driver = PostgresDriver(
            host=get_config().POSTGRES.HOST,
            port=get_config().POSTGRES.PORT,
            username=get_config().POSTGRES.USERNAME,
            password=get_config().POSTGRES.PASSWORD,
            db=get_config().POSTGRES.DB,
        )
        db_inject(_startup_repo, driver)
        db_inject(notes_repo, driver)
