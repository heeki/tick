import logging


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
