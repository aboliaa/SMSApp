from models.cache import cache

class OutboundProcessor(object):
    def __init__(self, data):
        self.data = data
        self.from_num = data['from']
        self.to_num = data['to']

    def process(self):
        if self._is_opted_out():
            error = 'sms from %s and to %s blocked by STOP request' \
                    %(self.from_num, self.to_num)
            raise ValueError(error)

    def _is_opted_out(self):
        if self._check_cache():
            print 'From %s and To %s pair is opted out' \
                  %(self.from_num, self.to_num)
            return True

    def _check_cache(self):
        key = '%s_%s' %(self.from_num, self.to_num)
        return cache.exists(key)