"""Pre-processing script for cleaning the raw rendered project."""
import subprocess
import sys


def install_package(package):
    """
    Installs desired package in current Python environment.

    Parameters
    ----------
    package: str
        Name of the package.

    """
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "--ignore-installed", package]
    )


def main():
    """Entry point of the script."""
    packages_list = ["isort"]
    for package in packages_list:
        install_package(package)


if __name__ == "__main__":
    main()
