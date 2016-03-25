import os
import inspect
import logging


CURRENT_DIR = os.path.dirname(
    os.path.abspath(
        inspect.getfile(inspect.currentframe())))


def _setup_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger


logger = _setup_logger()
