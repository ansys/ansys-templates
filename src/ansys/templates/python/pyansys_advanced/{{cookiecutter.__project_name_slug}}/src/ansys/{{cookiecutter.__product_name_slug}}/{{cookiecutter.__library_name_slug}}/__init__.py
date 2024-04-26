"""{{ cookiecutter.product_name }}.{{ cookiecutter.library_name }}"""

import importlib.metadata as importlib_metadata

__version__ = importlib_metadata.version(__name__.replace(".", "-"))
