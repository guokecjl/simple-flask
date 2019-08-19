# coding: utf-8

from redis import StrictRedis

from config import REDIS_CONFIG


def conn_redis(config):
    """
    redis 连接
    """
    cli = StrictRedis(host=config["host"],
                      port=config["port"],
                      db=config["database"],
                      password=config["password"],
                      socket_connect_timeout=2,
                      charset='utf-8')
    return cli


redis_cli = conn_redis(REDIS_CONFIG['auth'])
