import logging


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    fmt = logging.Formatter(u'[%(asctime)s] %(message)s')
    hdlr = logging.StreamHandler()
    hdlr.setFormatter(fmt)
    logger.addHandler(hdlr)
    return logger
