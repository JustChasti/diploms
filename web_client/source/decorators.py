from loguru import logger


def default_decorator(function):
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception as e:
            logger.exception(e)
            return False
    return wrapper
