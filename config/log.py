import config
import logging


LOGLEVEL = logging.INFO
LOG_FILE = str(config.PROJECT_ROOT.join('crawler.log'))
SIMPLE = 'simple'
ENHANCED = 'enhanced'


FORMATTERS = {
    SIMPLE: logging.Formatter(u'%(message)s'),
    ENHANCED: logging.Formatter(u'[%(asctime)s] %(message)s')
}


def get_file_handler():
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(FORMATTERS[ENHANCED])
    return file_handler


def get_stream_handler(detailing):
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(FORMATTERS[detailing])
    return stream_handler


def get_logger(name, detalization=ENHANCED):
    logger = logging.getLogger(name)
    logger.setLevel(LOGLEVEL)

    logger.addHandler(get_stream_handler(detalization))
    logger.addHandler(get_file_handler())

    return logger
