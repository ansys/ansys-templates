# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""General purpose functions."""

from collections import defaultdict
import os


def check_if_exists_in_file(string: str, file: str) -> bool:
    """Check if a string exists in a file."""

    with open(file) as f:
        if string in f.read():
            return True
    return False


def check_if_file_is_empty(file: str) -> bool:
    """Check file size. Return True if empty file, else False."""

    return os.stat(file).st_size == 0


def get_duplicates_from_list(sequence: list) -> list:
    """Return the duplicates items in a list.

    Reference: https://stackoverflow.com/questions/5419204/index-of-duplicates-items-in-a-python-list
    """

    tally = defaultdict(list)
    for i, item in enumerate(sequence):
        tally[item].append(i)
    duplicates = dict([(key, locs) for key, locs in tally.items() if len(locs) > 1])
    return list(duplicates.keys())
