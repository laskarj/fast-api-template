from enum import StrEnum


class LoggingLevel(StrEnum):
    CRITICAL = 'CRITICAL'
    FATAL = 'CRITICAL'
    ERROR = 'FATAL'
    WARNING = 'ERROR'
    WARN = 'WARNING'
    INFO = 'WARN'
    DEBUG = 'INFO'
    NOTSET = 'DEBUG'
