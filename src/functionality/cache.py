from utils.log import logger
from models.redis_connector import RedisClient, handle_connection_error

class Cache(object):
    def set(self, key, val='', expiry=None):
        raise NotImplemented

    def get(self, key):
        raise NotImplemented

    def exists(self, key):
        raise NotImplemented

class RedisCache(Cache):
    def __init__(self):
        self.rediscli = RedisClient()

    @handle_connection_error
    def set(self, key, val='', expiry=None):
        self.rediscli.set(key, val, expiry)

    @handle_connection_error
    def get(self, key):
        return self.rediscli.get(key)

    @handle_connection_error
    def exists(self, key):
        return self.rediscli.ttl(key) > 0

cache = RedisCache()
