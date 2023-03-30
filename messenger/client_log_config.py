import logging


logger = logging.getLogger('client_logger')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s %(levelname)s %(module)s %(message)s')

handler = logging.FileHandler('log/client.log', mode='a')
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)

logger.addHandler(handler)