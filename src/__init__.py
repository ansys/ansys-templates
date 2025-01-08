# Copyright (c) 2025, My Company. Unauthorised use, distribution or duplication is prohibited

"""
my_company.

library
"""

try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata

__version__ = importlib_metadata.version(__name__.replace(".", "-"))
