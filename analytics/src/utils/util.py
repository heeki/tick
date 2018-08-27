import logging
import time
from datetime import datetime


class Util:
    def __init__(self):
        pass

    @staticmethod
    def get_logger(name):
        log = logging.getLogger(name)
        log_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s '%(message)s'")
        handler_console = logging.StreamHandler()
        handler_console.setFormatter(log_formatter)
        log.setLevel(logging.INFO)
        if len(log.handlers) == 0:
            log.addHandler(handler_console)
        return log

    @staticmethod
    def get_timestamp():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def convert_timestamp(epoch):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(epoch))

    @staticmethod
    def get_epoch():
        return time.time()
