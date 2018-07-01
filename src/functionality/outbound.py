from functionality.cache import cache
from functionality.ratelimiter import ratelimit
from utils.log import logger

class OutboundProcessor(object):
    def __init__(self, data):
        self.data = data
        self.from_num = data['from']
        self.to_num = data['to']

    @ratelimit
    def process(self):
        logger.debug('Process %s' %self.data)
        if self._is_opted_out():
            error = 'sms from %s and to %s blocked by STOP request' \
                    %(self.from_num, self.to_num)
            raise ValueError(error)

    def _is_opted_out(self):
        """
        This function checks whether 'from' number is in cache,
        it means that number is opted out.
        """
        if self._check_cache():
            logger.warning('From %s and To %s pair is opted out' \
                  %(self.from_num, self.to_num))
            return True

    def _check_cache(self):
        key = '%s_%s' %(self.from_num, self.to_num)
        return cache.exists(key)