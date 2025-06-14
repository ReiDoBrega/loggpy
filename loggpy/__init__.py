# Custom log levels for Python's logging module
#
# Modder: ReiDoBrega
# Last Change: 02/03/2025

"""
Custom log levels for Python's :mod:`logging` module.
"""
import sys
import logging
import coloredlogs
from coloredlogs import DEFAULT_LEVEL_STYLES, DEFAULT_FIELD_STYLES
from typing import NoReturn, Optional, List, Dict, Any, Union

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


class LogFormat:
    MESSAGE = " {message}"
    ASCTIME = "{asctime} : {message}"
    DEFAULT = "{asctime} [{levelname[0]}] {name} : {message}"
    DETAILED = "{asctime} [{levelname}] {name} ({filename}:{lineno}) : {message}"
    SIMPLE = "[{levelname}] {message}"
    JSON = '{{"time": "{asctime}", "level": "{levelname}", "logger": "{name}", "message": "{message}"}}'

class Logger(logging.Logger):
    """
    Custom logger class supporting additional logging levels and pickling.

    Adds support for `notice()`, `spam()`, `success()`, `verbose()`,
    `logkey()`, and `exit()` methods. Can be used with serialization libraries.
    """
    LOG_FORMAT = "{asctime} [{levelname[0]}] {name} : {message}"
    LOG_DATE_FORMAT = '%Y-%m-%d %I:%M:%S %p'
    LOG_STYLE = "{"
    BLACKLIST: List[str] = []
    
    # Cache of logger instances
    _logger_instances = {}

    def __init__(self, name, level=logging.NOTSET):
        """
        Initialize a Logger object.

        :param name: The name of the logger.
        :param level: The logging level.
        """
        # Check if we already have a logger with this name
        if name in self._logger_instances:
            # Return existing logger's internal state
            existing = self._logger_instances[name]
            self.__dict__ = existing.__dict__.copy()
            return
            
        # Create a new logger
        super().__init__(name, level)
        self.parent = logging.getLogger()
        self._logger_instances[name] = self
    
    def __reduce__(self):
        return (self.__class__, (self.name,))
    
    def __getstate__(self):
        return {'name': self.name, 'level': self.level}
    
    def __setstate__(self, state):
        # Use the constructor to get a reference to an existing
        # or create a new logger with the same name
        self.__init__(state['name'], state['level'])

    @classmethod
    def mount(cls,
              level: Optional[int] = logging.INFO,
              logformat: Optional[LogFormat] = LogFormat.DEFAULT,
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
            
        cls.BLACKLIST = blacklist

        handlers = [logging.FileHandler(HandlerFilename, encoding='utf-8')] if HandlerFilename else [logging.StreamHandler()]

        logging.basicConfig(
            level=logging.DEBUG,
            format=logformat,
            datefmt=cls.LOG_DATE_FORMAT,
            style=cls.LOG_STYLE,
            handlers=handlers
        )

        for logger_name in blacklist:
            logging.getLogger(logger_name).setLevel(logging.WARNING)

        coloredlogs.install(
            level=level,
            fmt=logformat,
            datefmt=cls.LOG_DATE_FORMAT,
            handlers=[logging.StreamHandler()],
            style=cls.LOG_STYLE,
            field_styles=field_styles,
            level_styles=level_styles
        )
        
        # Set Logger as the default class for new loggers
        logging.setLoggerClass(cls)

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
            if isinstance(msg, str):
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
    'Logger', 'logging'
]

__version__ = '0.1.0'