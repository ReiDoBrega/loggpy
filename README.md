# loggpy

A powerful and flexible Python logging library that extends the standard logging module with custom log levels and colored output support.

## Features

- Custom log levels (NOTICE, SPAM, SUCCESS, VERBOSE, LOGKEY)
- Colored output support using `coloredlogs`
- Blacklist functionality to suppress specific loggers
- Customizable color schemes and formats
- File and console logging support
## Installation

```bash
pip install loggpy
```

## Basic Usage

```python
from loggpy import Logger
import logging

# Basic setup with console output
Logger.mount(level=logging.INFO)
log = Logger(__name__)

# Use standard log levels
log.debug("Debug message")
log.info("Info message")
log.warning("Warning message")
log.error("Error message")

# Use custom log levels
log.notice("Notice message")
log.spam("Spam message")
log.success("Success message")
log.verbose("Verbose message")
log.logkey("API Key: xyz123")  # For logging sensitive or key information
```

## Advanced Configuration

### Logging to File

```python
from pathlib import Path
from datetime import datetime

# Log to both console and file
Logger.mount(
    level=logging.DEBUG,
    HandlerFilename=Path("logs/app.log"),
)
```

### Dynamic Log File Names

```python
Logger.mount(
    level=logging.INFO,
    HandlerFilename=Path(
        f"logs/app_{datetime.now().strftime('%Y-%m-%d_%H_%M_%S')}.log"
    )
)
```

### Blacklisting Loggers

```python
# Suppress logs from specific modules
Logger.mount(
    level=logging.INFO,
    blacklist=[
        "filelock",
        "oauthlib",
        "google",
        "charset_normalizer"
    ]
)
```

### Custom Color Schemes

```python
Logger.mount(
    level=logging.INFO,
    field_styles={
        "asctime": {"color": 35},
        "name": {"color": 197},
        "levelname": {"color": 244, "bold": True},
    },
    level_styles={
        "spam": {"color": "green", "faint": True},
        "debug": {"color": 69},
        "verbose": {"color": "blue"},
        "info": {},
        "notice": {"color": "magenta"},
        "warning": {"color": "yellow"},
        "success": {"color": 67, "bold": True},
        "error": {"color": "red"},
        "critical": {"color": "red", "bold": True},
    }
)
```

## Log Levels

| Level    | Value | Description                                    |
|----------|-------|------------------------------------------------|
| SPAM     | 5     | Even more detailed than DEBUG                  |
| VERBOSE  | 15    | Between DEBUG and INFO                         |
| LOGKEY   | 21    | Important key information or sensitive data    |
| NOTICE   | 25    | Normal but significant events                  |
| SUCCESS  | 35    | Successful operations                          |

## Full Example

```python
from loggpy import Logger
import logging
from pathlib import Path

def setup_logging(debug_mode=False):
    # Configure logging with custom settings
    Logger.mount(
        level=logging.DEBUG if debug_mode else logging.INFO,
        HandlerFilename=Path("logs/app.log"),
        blacklist=["filelock", "oauthlib"],
        field_styles={
            "asctime": {"color": 35},
            "name": {"color": 197},
            "levelname": {"color": 244, "bold": True},
        },
        level_styles={
            "spam": {"color": "green", "faint": True},
            "debug": {"color": 69},
            "verbose": {"color": "blue"},
            "success": {"color": 67, "bold": True},
        }
    )

    return Logger(__name__)

# Initialize logger
log = setup_logging(debug_mode=True)

# Example usage
log.spam("Starting application initialization...")
log.debug("Loading configuration...")
log.verbose("Configuration loaded successfully")
log.info("Application started")
log.notice("New user connected")
log.logkey("Session token: 8f7d56a2-bc4d-4c12-a891-45e70542b21f")
log.success("Transaction completed successfully")
log.warning("High memory usage detected")
log.error("Failed to connect to database")
log.critical("System shutdown initiated")
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built on top of Python's standard `logging` module
- Uses `coloredlogs` for terminal color support
