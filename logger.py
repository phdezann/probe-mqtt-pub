import logging


def configure_logger(level):
    logging.basicConfig(level=level, format='%(asctime)s [%(process)d] [%(threadName)s] [%(levelname)s] %(message)s')
