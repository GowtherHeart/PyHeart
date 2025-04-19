import sys

from loguru import logger


class LoggingInit:
    def __init__(self, lvl: str) -> None:
        logger.remove()
        logger.add(
            sys.stdout,
            format=self.format(),
            level=lvl,
            enqueue=True,
        )

    def format(self) -> str:
        return (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> || <lvl>{level}</lvl> || "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> || "
            "[ID-{extra[request_id]}] {message}"
        )
