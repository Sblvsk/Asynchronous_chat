import logging
import logging.handlers

logger = logging.getLogger('server')
logger.setLevel(logging.DEBUG)

handler = logging.FileHandler('server.log')
handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)