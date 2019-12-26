import json
import logging
import logging.config
import os

from ._my_logger import lazy_loader


class MyLogger(object):
    def __init__(self, name: str):
        file_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "logging.json"
        )
        logging.config.dictConfig(json.load(open(file_path)))
        self.name = name
        self.logger = None

    def init(self):
        self.logger = logging.getLogger(self.name)

    @lazy_loader
    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, exc_info=True, extra={"additional_data": kwargs})

    @lazy_loader
    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, exc_info=True, extra={"additional_data": kwargs})

    @lazy_loader
    def warning(self, msg, *args, **kwargs):
        self.logger.warning(
            msg, *args, exc_info=True, extra={"additional_data": kwargs}
        )

    @lazy_loader
    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, exc_info=True, extra={"additional_data": kwargs})
