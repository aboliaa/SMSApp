import logging
from config import LOGLEVEL

handler = logging.StreamHandler()
logger = logging.getLogger()
logger.setLevel(LOGLEVEL)
logger.addHandler(handler)
