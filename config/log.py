import logging


LOGLEVEL = logging.DEBUG


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(LOGLEVEL)
    fmt = logging.Formatter(u'[%(asctime)s] %(message)s')
    hdlr = logging.StreamHandler()
    hdlr.setFormatter(fmt)
    logger.addHandler(hdlr)
    return logger
