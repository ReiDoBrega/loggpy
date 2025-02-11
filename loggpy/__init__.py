# Custom log levels for Python's logging module.
#
# Modder: ReiDoBrega
# Last Change: 11/02/2025

"""
Custom log levels for Python's :mod:`logging` module.
"""
import sys
import logging
import coloredlogs
from coloredlogs import DEFAULT_LEVEL_STYLES, DEFAULT_FIELD_STYLES
from typing import NoReturn, Optional, List, Dict, Any

# Define custom log levels
NOTICE = 25
SPAM = 5
SUCCESS = 35
VERBOSE = 15
LOGKEY = 21

# Register custom log levels
for level, name in [
    (NOTICE, 'NOTICE'),
    (SPAM, 'SPAM'),
    (SUCCESS, 'SUCCESS'),
    (VERBOSE, 'VERBOSE'),
    (LOGKEY, 'LOGKEY')
]:
    logging.addLevelName(level, name)
    setattr(logging, name, level)


class Logger(logging.Logger):
    """
    Custom logger class supporting additional logging levels.

    Adds support for `notice()`, `spam()`, `success()`, `verbose()`,
    `logkey()`, and `exit()` methods.
    """
    LOG_FORMAT = "{asctime} [{levelname[0]}] {name} : {message}"
    LOG_DATE_FORMAT = '%Y-%m-%d %I:%M:%S %p'
    LOG_STYLE = "{"
    BLACKLIST: List[str] = []

    def __init__(self, *args, **kwargs):
        """
        Initialize a Logger object.

        :param args: Arguments passed to superclass (logging.Logger).
        :param kwargs: Keyword arguments passed to superclass (logging.Logger).
        """
        super().__init__(*args, **kwargs)
        self.parent = logging.getLogger()

    @classmethod
    def mount(cls,
              level: Optional[int] = logging.INFO,
              HandlerFilename: Optional[str] = "",
              blacklist: Optional[List[str]] = None,
              field_styles: Optional[Dict[str, Any]] = DEFAULT_FIELD_STYLES,
              level_styles: Optional[Dict[str, Any]] = DEFAULT_LEVEL_STYLES) -> None:
        """
        Configure the logging system.

        :param level: The logging level.
        :param HandlerFilename: The path to the log file. If empty, logs to stdout.
        :param blacklist: A list of logger names to suppress.
        :param field_styles: Custom field styles for coloredlogs.
        :param level_styles: Custom level styles for coloredlogs.
        """
        if blacklist is None:
            blacklist = []

        handlers = [logging.FileHandler(HandlerFilename, encoding='utf-8')] if HandlerFilename else [logging.StreamHandler()]

        logging.basicConfig(
            level=logging.DEBUG,
            format=cls.LOG_FORMAT,
            datefmt=cls.LOG_DATE_FORMAT,
            style=cls.LOG_STYLE,
            handlers=handlers
        )

        for logger_name in blacklist:
            logging.getLogger(logger_name).setLevel(logging.WARNING)

        coloredlogs.install(
            level=level,
            fmt=cls.LOG_FORMAT,
            datefmt=cls.LOG_DATE_FORMAT,
            handlers=[logging.StreamHandler()],
            style=cls.LOG_STYLE,
            field_styles=field_styles,
            level_styles=level_styles
        )

    def log(self, level: int, msg: object, *args: object, **kwargs) -> None:
        """
        Log a message with the specified level.

        :param level: The logging level.
        :param msg: The message to log.
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        """
        if self.name in self.BLACKLIST:
            level = logging.DEBUG

        if self.name.startswith("seleniumwire") and level <= logging.INFO:
            level = logging.DEBUG

        if self.name.startswith("urllib3"):
            if msg.startswith("Incremented Retry"):
                level = logging.WARNING
            elif level == logging.DEBUG:
                level = VERBOSE

            if msg == '%s://%s:%s "%s %s %s" %s %s':
                scheme, host, port, method, url, protocol, status, reason = args
                if (scheme == "http" and port == 80) or (scheme == "https" and port == 443):
                    msg = "%s %s://%s%s %s %s %s"
                    args = (method, scheme, host, url, protocol, status, reason)
                else:
                    msg = "%s %s://%s:%s%s %s %s %s"
                    args = (method, scheme, host, port, url, protocol, status, reason)

        super().log(level, msg, *args, **kwargs)

    def notice(self, msg: str, *args, **kwargs) -> None:
        """Log a message with level NOTICE."""
        if self.isEnabledFor(NOTICE):
            self.log(NOTICE, msg, *args, **kwargs)

    def spam(self, msg: str, *args, **kwargs) -> None:
        """Log a message with level SPAM."""
        if self.isEnabledFor(SPAM):
            self.log(SPAM, msg, *args, **kwargs)

    def success(self, msg: str, *args, **kwargs) -> None:
        """Log a message with level SUCCESS."""
        if self.isEnabledFor(SUCCESS):
            self.log(SUCCESS, msg, *args, **kwargs)

    def verbose(self, msg: str, *args, **kwargs) -> None:
        """Log a message with level VERBOSE."""
        if self.isEnabledFor(VERBOSE):
            self.log(VERBOSE, msg, *args, **kwargs)

    def logkey(self, msg: str, *args, **kwargs) -> None:
        """Log a message with level LOGKEY."""
        if self.isEnabledFor(LOGKEY):
            self.log(LOGKEY, msg, *args, **kwargs)

    def exit(self, msg: str, *args, **kwargs) -> NoReturn:
        """
        Log a message with severity 'CRITICAL' and terminate the program.

        :param msg: The message to log.
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        """
        self.critical(msg, *args, **kwargs)
        sys.exit(1)


__all__ = [
    'Logger', 'install', 'logging'
]

__version__ = '0.0.9'