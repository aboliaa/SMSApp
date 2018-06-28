from config import OPT_OUT_STR, CACHE_EXPIRY
from models.cache import cache

class InboundProcessor(object):
    def __init__(self, data):
        self.data = data
        self.from_num = data['from']
        self.to_num = data['to']
        self.text = data['text'].strip()

    def process(self):
        self._opt_out_if_set()

    def _opt_out_if_set(self):
        if self.text == OPT_OUT_STR:
            print 'As text is STOP, Opt out for configured expiry time'
            self._cache_numbers()

    def _cache_numbers(self):
        key = '%s_%s' %(self.from_num, self.to_num)
        cache.set(key, expiry=CACHE_EXPIRY)