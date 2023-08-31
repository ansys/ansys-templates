# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""Common functions."""

from pathlib import Path
from typing import Union

from ansys.optislang.core import utils


def get_available_optislang_installations(output_format: str = "short") -> list:
    """Return a list of available optiSLang installations."""

    versions = list(dict(utils.find_all_osl_exec()).keys())

    if output_format == "short":
        return versions
    elif output_format == "long":
        return [convert_to_long_version(version) for version in versions]
    else:
        raise ValueError("Argument output_format takes one of these two values: short, long.")


def get_optislang_executable(version: Union[int, str]) -> Path:
    """Return the path to OptiSLang executable."""

    version = convert_to_short_version(version)

    if utils.get_osl_exec(version):
        return utils.get_osl_exec(version)[1]
    else:
        raise Exception(f"optiSLang {version} not found.")


def is_long_version(long_version: str) -> bool:
    """Check if the long version syntax is correct."""
    try:
        long_version_parts = long_version.split(".")
    except:
        return False
    if len(long_version_parts) == 2:
        if len(long_version_parts[0]) == 4 and len(long_version_parts[1]) == 1:
            if long_version_parts[0].startswith("20") and long_version_parts[1] in ["1", "2"]:
                pass
            else:
                return False
        else:
            return False
    else:
        return False
    return True


def is_short_version(short_version: Union[str, int]) -> bool:
    """Check if the short version syntax is correct."""
    if len(short_version) == 3 and short_version.isdigit():
        return True
    else:
        return False


def convert_to_long_version(short_version: Union[str, int]) -> str:
    """Convert a product version to long format."""
    short_version = str(short_version)
    if is_long_version(short_version):
        return short_version
    elif is_short_version(short_version):
        return "20" + short_version[:-1] + "." + short_version[-1]
    else:
        raise Exception(f"Version {short_version} is not recognized as a short version.")


def convert_to_short_version(long_version: str) -> str:
    """Convert a product version to short format."""

    if is_short_version(long_version):
        return long_version
    elif is_long_version(long_version):
        return long_version[2:].replace(".", "")
    else:
        raise Exception(f"Version {long_version} is not recognized as a long version.")


def check_version_syntax(version: str) -> None:
    """Throw an error if the version syntax is unknown."""

    if is_short_version(version):
        pass
    elif is_long_version(version):
        version = convert_to_short_version(version)
    else:
        raise Exception(f"Unknown format for product version: {version}.")
