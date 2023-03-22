import logging
import inspect

logger = logging.getLogger('decorator_logger')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(message)s')

def log(func):
    def wrapper(*args, **kwargs):
        caller = inspect.stack()[1][3]
        logger.info(f'Function {func.__name__} called from {caller}')
        return func(*args, **kwargs)
    return wrapper