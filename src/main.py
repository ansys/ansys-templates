# Copyright (c) 2022, My Company. Unauthorised use, distribution or duplication is prohibited


"""
my_company.

library
"""

from datetime import datetime

from logger import Logger

logger = Logger.init("my_company.library")


def get_date_and_time():
    """Compute today's datetime."""
    return datetime.today().strftime("%Y-%m-%d-%H:%M:%S")


if __name__ == "__main__":
    logger.info(f"Hello! Welcome, we are {get_date_and_time()}")
