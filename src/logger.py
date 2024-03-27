"""Logger module."""
# Copyright (c) 2024, My Company. Unauthorised use, distribution or duplication is prohibited

from datetime import datetime
import logging
import os


class Logger(object):
    """Logger class."""

    @classmethod
    def init(cls, name):
        """Initialize Logger instances."""
        formatter = logging.Formatter(
            "%(asctime)s %(name)s %(levelname)s %(threadName)-10s %(message)s"
        )

        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        filename = "{0}.log".format(datetime.today().strftime("%Y_%m_%d@%H_%M_%S"))

        if os.name != "nt":
            filepath = f"/var/log/{filename}"
        else:
            folder = os.path.join(os.getenv("LOCALAPPDATA"), "my_company", "library")
            if not os.path.exists(folder):
                os.makedirs(folder)
            filepath = os.path.join(folder, filename)
        fh = logging.FileHandler(filepath)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        return logger