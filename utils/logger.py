"""
This module is used to setup the logger for the project.
The logger features a custom formatter that adds color to the output.
"""

import logging
from dotenv import dotenv_values

env_config = dotenv_values(".env")

class CustomFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: "\x1b[38;20m",       # gray
        logging.INFO: "\x1b[36m",           # cyan
        logging.WARNING: "\x1b[33;20m",     # yellow
        logging.ERROR: "\x1b[31;20m",       # red
        logging.CRITICAL: "\x1b[31;1m",     # bold red
    }
    RESET = "\x1b[0m"
    FORMAT = (
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    )

    def format(self, record):
        log_fmt = self.COLORS.get(record.levelno, self.RESET) + self.FORMAT + self.RESET
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def setup_logger():
    logger = logging.getLogger(env_config["PROJECT_ID"])
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(CustomFormatter())
    logger.addHandler(ch)
    return logger
