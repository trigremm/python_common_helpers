# helpers/loggers.py
import sys

from loguru import logger

# Export the loggers for use in other modules
__all__ = ["logger"]

# Default logger configuration
logger.remove()

logger.add(sys.stderr, level="INFO", enqueue=True)

logger.add(
    "app.log",
    level="SUCCESS",
    format="{time} {module}.{function}:{line} {level} {message}",
    rotation="10 MB",
    enqueue=True,
    compression="zip",
)
