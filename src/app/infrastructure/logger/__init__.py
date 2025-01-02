import logging

from .enums import LoggingLevel
from .formatters import MainConsoleFormatter


def setup(logining_lvl: LoggingLevel) -> None:
    logging_level = logging.getLevelName(logining_lvl)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging_level)
    console_handler.setFormatter(MainConsoleFormatter())
    logging.basicConfig(handlers=[console_handler], level=logging_level)
