import requests
import time
from .logger import Logger


class Base(object):
    def __init__(self):
        self.headers = {"Connection": "keep-alive",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
                        }

    def open_page(self, url):
        result = requests.get(url, self.headers)
        Logger.info(result)


Base = Base()
