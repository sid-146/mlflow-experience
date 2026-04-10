import logging
import os
from datetime import datetime

level = logging.DEBUG


class ColoredFormatter(logging.Formatter):
    """
    Formatter that adds colors to log levels for console output.
    """

    COLORS = {
        "DEBUG": "\033[94m",  # Blue
        "INFO": "\033[92m",  # Green
        "WARNING": "\033[93m",  # Yellow
        "ERROR": "\033[91m",  # Red
        "CRITICAL": "\033[95m",  # Magenta
    }

    RESET = "\033[0m"

    def format(self, record):
        original_levelname = record.levelname

        if original_levelname in self.COLORS:
            record.levelname = f"{self.COLORS[original_levelname]} \
                {original_levelname}{self.RESET}"

        message = super().format(record)

        record.levelname = original_levelname
        return message


"""
    Path setup
"""
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")

os.makedirs(LOG_DIR, exist_ok=True)

filename = f"logs_{datetime.now().strftime('%Y_%m_%d_%H_%M')}.log"
filepath = os.path.join(LOG_DIR, filename)


"""
    Handlers
"""
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler(filepath, mode="a")


"""
    Formatters
"""
c_format = ColoredFormatter(
    "%(levelname)s: %(asctime)s : %(module)s/%(filename)s : [%(funcName)s] : %(lineno)d : %(message)s"
)

f_format = logging.Formatter(
    "%(asctime)s : [%(levelname)s] : %(module)s : [%(funcName)s] : %(lineno)d : %(message)s"
)

c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

c_handler.setLevel(level)
f_handler.setLevel(level)


"""
    Console Logger
"""
console = logging.getLogger("console")
console.setLevel(level)
console.propagate = False

# Avoid duplicate handlers if module is imported multiple times
if not console.handlers:
    console.addHandler(c_handler)
    console.addHandler(f_handler)


__all__ = ["console"]
