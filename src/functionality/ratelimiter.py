import time
import uuid
from functools import wraps
from utils.log import logger

from models.redis_connector import RedisClient, handle_connection_error
from config import RATELIMITING_EXPIRY, RATELIMITING_PER_ITEMS

class MaxLimitReachedError(Exception):
    pass

def get_request_id():
    return uuid.uuid4()


class RateLimiter(object):
    """
    This ratelimiter is implemented using leaky bucket algorithm.
    https://en.wikipedia.org/wiki/Leaky_bucket

    1. A bucket will be maintained for each from number.
    2. Each bucket can hold maximum upto N requests.
    3. Whenever a new request comes for a from number, if its bucket is already full,
    raise MaxLimitReachedError.
    4. Otherwise, add the request in the bucket (request will be served).
    5. Each request will be removed from the bucket when it completes time T in the bucket.

    Buckets are implemented using Redis sorted sets.
    - Sorted sets are Redis sets where each member can be assigned a score with it.
    - Request will be added in a set with timestamp associated with it as it's score.
    - When a new request comes, memebers with timestamp older than expiry time
    will be deleted.
    - If at any point of time, total members in a set are greater than max permitted
    requests, error will be raised.

    'from_num' is key for sorted set
    'request_id' is member of sorted set
    'timestamp' is maintained as score for 'request_id'
    """

    def __init__(self):
        self.redis = RedisClient()
        self.expiry_time = RATELIMITING_EXPIRY
        self.max_items = RATELIMITING_PER_ITEMS

    def check_ratelimiting(self, from_num):
        request_id = get_request_id()
        timestamp = int(time.time())

        self.expire_old_requests(from_num, timestamp)
        if self.is_limit_reached(from_num):
            raise MaxLimitReachedError('Limit reached for from %s' %from_num)

        self.add_request(from_num, timestamp, request_id)

    def add_request(self, from_num, timestamp, request_id):
        self.redis.zadd(from_num, timestamp, request_id)

        logger.debug('[Rate-Limiter {}] Request-id {} is added in ratelimiter set with timestamp {}'
                     .format(from_num, request_id, timestamp))

    def expire_old_requests(self, from_num, timestamp):
        expire_before = timestamp - self.expiry_time
        self.redis.zremrangebyscore(from_num, 0, expire_before)

        logger.debug('[Rate-Limiter {}] Request-ids with timestamp less than {} are deleted'
                 .format(from_num, timestamp))

    def is_limit_reached(self, from_num):
        count = self.redis.zcard(from_num)
        if count >= self.max_items:
            logger.debug('[Rate-Limiter {}] Limit reached'
                         .format(from_num))
            return True
        return False

limiter = RateLimiter()

def ratelimit(func):
    @wraps(func)
    def decorater(self, *args, **kwargs):
        # This decorator is written considering it will be applied to class
        # method. Hence, 'from_num' is fetched from 'self'. It can be decoupled
        # from input parameters of the function.
        limiter.check_ratelimiting(self.from_num)
        return func(self, *args, **kwargs)
    return decorater