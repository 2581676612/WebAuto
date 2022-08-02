import logging
import sys


class Logger(object):
    def __init__(self):
        self.log_format = '%(asctime)s - %(levelname)s - %(message)s'
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        # self.init()

    def init(self):
        # 输出到控制台
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(logging.Formatter(self.log_format))
        self.logger.addHandler(handler)
        # 输出到文件


    def info(self, msg=None):
        self.logger.info(msg)

    def error(self, msg=None):
        self.logger.error(msg)


Logger = Logger()
