from src.config.app import get_config
from src.pkg.driver.redis import RedisDriver


def core_redis():
    return RedisDriver(
        host=get_config().REDIS.HOST,
        port=get_config().REDIS.PORT,
        username=get_config().REDIS.USERNAME,
        password=get_config().REDIS.PASSWORD,
        db=get_config().REDIS.DB,
    )
