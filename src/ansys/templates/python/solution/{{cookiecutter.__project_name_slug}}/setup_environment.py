# ©2022, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""
A Python script to setup the Python ecosystem of a solution or framework.

Platform      : OS independent
Python version: >= 3.7, <= 3.9

"""

# ==================================================== [Imports] ==================================================== #

import argparse
import os
from pathlib import Path, PurePath
import platform
import shutil
import subprocess
import sys
import textwrap
import time

try:
    import toml
except:
    subprocess.run(f"{sys.executable} -m pip install toml", check=True)
    import toml

# =================================================== [Functions] =================================================== #


def get_python_version():
    """Get Python version."""
    return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"


def parser():
    """Parse command line arguments."""
    # Code Name
    program_name = "Setup Environment"
    # Code description
    program_description = "A Python script to setup the Python ecosystem of a solution or framework."
    # Create top-level parser
    parser = argparse.ArgumentParser(
        prog=program_name,
        usage=None,
        prefix_chars="-",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(program_description),
    )
    parser._action_groups.pop()
    # Definition of the group of arguments
    required_inputs = parser.add_argument_group("Required arguments")
    optional_inputs = parser.add_argument_group("Optional arguments")
    # Optional parameters
    optional_inputs.add_argument(
        "-d",
        "--dependencies",
        type=str,
        nargs="+",
        help="List of dependency types to be installed.",
        default=[],
        choices=["run", "doc", "tests", "build", "style", "all"],
        required=False,
    )
    optional_inputs.add_argument(
        "-b", "--build-system", type=str, help="Build system", default="poetry", choices=["poetry"], required=False
    )
    optional_inputs.add_argument(
        "-s", "--build-system-version", type=str, help="Build system version", default="*", required=False
    )
    optional_inputs.add_argument(
        "-B", "--build", help="builds the source and wheels archive", action="store_true", required=False
    )
    optional_inputs.add_argument(
        "-m",
        "--build-method",
        type=str,
        help="Build system",
        default="build-system",
        choices=["build-system", "build"],
        required=False,
    )
    optional_inputs.add_argument(
        "-c",
        "--credentials-management",
        type=str,
        help="Method to store private sources credentials.",
        default="keyring",
        choices=["keyring", "env-vars"],
        required=False,
    )
    optional_inputs.add_argument(
        "-S",
        "--sources-directory",
        type=Path,
        help="Path to sources directory.",
        default=Path(__file__).parent.parent.absolute() / "src",
        required=False,
    )
    optional_inputs.add_argument(
        "-P",
        "--package-data",
        type=Path,
        nargs="+",
        help="Paths to package data to include.",
        default=[],
        required=False,
    )
    optional_inputs.add_argument(
        "-e", "--venv-name", type=str, help="Name of the virtual environment.", default=".venv", required=False
    )
    optional_inputs.add_argument(
        "-n",
        "--no-clear",
        help="No workspace clean-up. Work with existing .venv if exists.",
        action="store_true",
        required=False,
    )

    return parser.parse_args()


def check_inputs(args):
    """Check inputs consistency."""
    # Rework dependencies argument if all option is selected
    if "all" in args.dependencies:
        args.dependencies = ["run", "doc", "tests", "build", "style"]
    # Activate build dependencies if build is required
    if args.build:
        if "run" not in args.dependencies and args.build_method == "build-system":
            args.dependencies.append("run")
        if "build" not in args.dependencies:
            args.dependencies.append("build")
    # Check if configuration file is available when run dependencies are activated
    if "run" in args.dependencies:
        if not os.path.exists("pyproject.toml"):
            raise FileNotFoundError(
                "%s require a configuration file. No %s file detected."
                % (args.build_system.title(), configuration_file)
            )
    # Check if requirement file is available when optional dependencies are activated
    for requirement_type in ["doc", "tests", "build", "style"]:
        if requirement_type in args.dependencies:
            requirement_file = f"requirements/requirements_{requirement_type}.txt"
            if not os.path.exists(requirement_file):
                raise FileNotFoundError(f"Missing {requirement_file}")
    # Convert package data paths to absolute
    for i, data in enumerate(args.package_data):
        args.package_data[i] = os.path.abspath(data)
        if not os.path.exists(args.package_data[i]):
            raise FileNotFoundError("No such file or directory: %s." % (args.package_data[i]))
    # Convert sources directory path to absolute
    if args.package_data:
        args.sources_directory = os.path.abspath(args.sources_directory)
        if not os.path.isdir(args.sources_directory):
            raise FileNotFoundError("Path to sources directory is missing: %s." % (args.sources_directory))
    # Check virtual environment name if Poetry is used
    if args.build_system == "poetry":
        if args.venv_name != ".venv":
            old_name = args.venv_name
            args.venv_name = ".venv"
            sys.stdout.write(
                "Warning: Poetry expects the name of the virtual environment name to be .venv.\n%s is renamed %s.\n"
                % (old_name, args.venv_name)
            )
    # Check if src structure is defined
    if "run" in args.dependencies:
        if os.path.exists(args.sources_directory):
            contains_python = False
            for path, dirs, files in os.walk(args.sources_directory):
                for file in files:
                    if file.endswith(".py"):
                        contains_python = True
                        break
            if not contains_python:
                raise Exception("Source directory contains no Python files.")
        else:
            raise FileExistsError(f"Source directory {args.sources_directory} does not exist.")
    # Check TOML consistency
    if "run" in args.dependencies:
        package_config = toml.load("pyproject.toml")
        if "readme" in package_config["tool"]["poetry"].keys():
            readme_file = package_config["tool"]["poetry"]["readme"]
            if not os.path.exists(readme_file):
                raise FileNotFoundError(
                    "A README file is declared in the configuration file but is missing in the project."
                )


def show_parameters(args):
    """Display the parameters to the console before proceeding to work."""
    sys.stdout.write("OS                       : %s\n" % (platform.system()))
    sys.stdout.write("Python version           : %s\n" % (get_python_version()))
    sys.stdout.write("Virtual environment name: %s\n" % (args.venv_name))
    sys.stdout.write("Run dependencies         : %s\n" % ("yes" if "run" in args.dependencies else "no"))
    sys.stdout.write("Doc dependencies         : %s\n" % ("yes" if "doc" in args.dependencies else "no"))
    sys.stdout.write("Tests dependencies       : %s\n" % ("yes" if "tests" in args.dependencies else "no"))
    sys.stdout.write("Build dependencies       : %s\n" % ("yes" if "build" in args.dependencies else "no"))
    sys.stdout.write("Style dependencies       : %s\n" % ("yes" if "style" in args.dependencies else "no"))
    sys.stdout.write("Build system             : %s\n" % (args.build_system))
    sys.stdout.write("Build system version     : %s\n" % (args.build_system_version))
    sys.stdout.write("Build distribution       : %s\n" % ("yes" if args.build else "no"))
    sys.stdout.write("Build method             : %s\n" % (args.build_method))
    sys.stdout.write("Credentials management   : %s\n" % (args.credentials_management))
    sys.stdout.write("\n")


def clear_workspace(args):
    """Remove residual items form previous installation (like venv directory, lock file ...)."""
    if not args.no_clear:
        # Remove virtual environment
        if os.path.isdir(".venv"):
            sys.stdout.write("Delete existing virtual environment\n")
            shutil.rmtree(".venv")
        # Remove lock file
        if os.path.isfile("poetry.lock"):
            sys.stdout.write("Delete existing poetry lock file\n")
            os.remove("poetry.lock")


def get_private_sources(config_file):
    """Get list of private sources from configuration file."""
    package_config = toml.load(config_file)
    try:
        private_sources = package_config["tool"]["poetry"]["source"]
    except:
        private_sources = []
    return private_sources


def get_package_data(config_file):
    """Get list of package data to include in the source distribution."""
    package_config = toml.load(config_file)
    try:
        package_data = package_config["tool"]["poetry"]["include"]
    except:
        package_data = []
    return package_data


def configure_build_system(args):
    """Configure the build system to enable connection to private sources."""
    # Turn-on in-project
    subprocess.run([".venv/Scripts/poetry", "config", "virtualenvs.in-project", "true"])

    # Configure credentials for private package sources
    # Get list of private sources
    private_sources = get_private_sources("pyproject.toml")
    # Delete existing configuration
    sys.stdout.write("Clean-up existing poetry configurations\n")
    if sys.platform == "win32":
        username = os.getlogin()
        path_poetry_config = r"C:\Users\%s\AppData\Roaming\pypoetry" % (username)
        if os.path.isfile(os.path.join(path_poetry_config, "config.toml")):
            os.remove(os.path.join(path_poetry_config, "config.toml"))
        if os.path.isfile(os.path.join(path_poetry_config, "auth.toml")):
            os.remove(os.path.join(path_poetry_config, "auth.toml"))
    else:
        raise Exception("Implementation not ready.")
    # Declare credentials for private sources
    for source in private_sources:
        sys.stdout.write("Declare credentials for %s\n" % (source["name"]))
        # Get source PAT
        if source["url"] == "https://pkgs.dev.azure.com/pyansys/_packaging/pyansys/pypi/simple/":
            token = os.environ["PYANSYS_PRIVATE_PYPI_PAT"]
        elif source["url"] == "https://pkgs.dev.azure.com/pyansys/_packaging/ansys-solutions/pypi/simple/":
            token = os.environ["SOLUTIONS_PRIVATE_PYPI_PAT"]
        else:
            raise Exception("Unknown private source %s with url %s." % (source["name"], source["url"]))
        # Store credentials
        if args.credentials_management == "keyring":
            command = ".venv/Scripts/poetry config repositories.%s %s" % (source["name"], source["url"])
            subprocess.run(command)
            command = ".venv/Scripts/poetry config http-basic.%s PAT %s" % (source["name"], token)
            subprocess.run(command)
        elif args.credentials_management == "env-vars":
            # Format source name to comply with Poetry environment variable syntax
            source_name = source["name"].upper().replace("-", "_")
            # Create Poetry environment variable
            os.environ[f"POETRY_HTTP_BASIC_{source_name}_USERNAME"] = "PAT"
            os.environ[f"POETRY_HTTP_BASIC_{source_name}_PASSWORD"] = token
    return


def install_package_dependencies(args):
    """Install the package (mandatory requirements only)."""
    subprocess.run([".venv/Scripts/poetry", "install", "-vvv"], check=True)


def install_optional_dependencies(dependency_group):
    """Install optional requirements (doc, tests, build or style)."""
    file = os.path.join("requirements", f"requirements_{dependency_group}.txt")
    command = f".venv/Scripts/python -m pip install -r {file}"
    subprocess.run(command, check=True)


def include_package_data(args):
    """Move package data in the source directory to include them in the source distribution."""
    # Move package data to project sources
    for data in args.package_data:
        if os.path.isfile(data):
            shutil.copy(data, args.sources_directory)
        elif os.path.isdir(data):
            destination = os.path.join(args.sources_directory, PurePath(data).name)
            try:
                shutil.copytree(data, "%s" % (destination))
            except:
                sys.stdout.write("Warning: package_data %s exists in %s. No override.\n" % (data, destination))
        else:
            raise FileNotFoundError("No such file or directory : %s" % (data))


def build_distribution(args):
    """Build the source and wheels archives."""
    if args.build_method == "build-system":
        subprocess.run([".venv/Scripts/poetry", "build", "-vvv"], check=True)
    elif args.build_method == "build":
        subprocess.run([".venv/Scripts/python", "-m", "build"], check=True)
    else:
        raise ValueError("Unknown build method %s." % (args.build_method))


def main():
    """Sequence of operations leading to the complete Python ecosystem."""
    # Start timer
    time_on = time.time()
    # Get current working directory
    working_directory = os.getcwd()
    # Get installation directory
    install_directory = Path(__file__).parent.absolute()
    # Move to install directory
    os.chdir(install_directory)
    # Read command line inputs
    args = parser()
    # Check inputs consistency
    check_inputs(args)

    # Display header
    sys.stdout.write("==============================================================================================\n")
    sys.stdout.write("Setup Environment\n")
    sys.stdout.write("==============================================================================================\n")
    sys.stdout.write("\n")

    sys.stdout.write("\n")
    sys.stdout.write("Setup session --------------------------------------------------------------------------------\n")
    sys.stdout.write("\n")

    # Parameters
    show_parameters(args)

    # Clean-up workspace
    clear_workspace(args)

    sys.stdout.write("\n")
    sys.stdout.write("Setup virtual environment --------------------------------------------------------------------\n")
    sys.stdout.write("\n")

    # Create virtual environment
    sys.stdout.write("Create virtual environment\n")
    if os.path.isdir(args.venv_name) and args.no_clear:
        sys.stdout.write("Skipped\n")
    else:
        subprocess.run([sys.executable, "-m", "venv", ".venv"])
    sys.stdout.write("\n")

    # Upgrade to latest pip version
    sys.stdout.write("Upgrade to latest pip version\n")
    subprocess.run([".venv/Scripts/python", "-m", "pip", "install", "--upgrade", "pip"])
    sys.stdout.write("\n")

    sys.stdout.write("Setup build system ---------------------------------------------------------------------------\n")
    sys.stdout.write("\n")

    # Install build system
    sys.stdout.write("Install build system\n")
    if "run" in args.dependencies:
        command = ".venv/Scripts/python -m pip install %s" % (args.build_system)
        if args.build_system_version != "*":
            command += "==%s" % (args.build_system_version)
        subprocess.run(command, check=True)
    else:
        sys.stdout.write("Skipped\n")
    sys.stdout.write("\n")

    # Configure build system
    sys.stdout.write("Configure build system\n")
    if "run" in args.dependencies:
        configure_build_system(args)
    else:
        sys.stdout.write("Skipped\n")
    sys.stdout.write("\n")

    sys.stdout.write("Install requirements -------------------------------------------------------------------------\n")
    sys.stdout.write("\n")

    # Install package dependencies
    sys.stdout.write("Install run dependencies\n")
    if "run" in args.dependencies:
        install_package_dependencies(args)
    else:
        sys.stdout.write("Skipped\n")
    sys.stdout.write("\n")

    # Install optional dependencies
    for dependency_group in ["doc", "tests", "build", "style"]:
        sys.stdout.write("Install %s dependencies\n" % (dependency_group))
        if dependency_group in args.dependencies:
            install_optional_dependencies(dependency_group)
        else:
            sys.stdout.write("Skipped\n")
        sys.stdout.write("\n")

    sys.stdout.write("Build distribution ---------------------------------------------------------------------------\n")
    sys.stdout.write("\n")

    # Build distribution
    if args.build:
        # Include package data
        sys.stdout.write("Include package data\n")
        include_package_data(args)
        sys.stdout.write("\n")
        # Build distribution
        sys.stdout.write("Build distribution\n")
        build_distribution(args)
        sys.stdout.write("\n")
    else:
        sys.stdout.write("Skipped\n")
    sys.stdout.write("\n")

    # Back to current working directory
    os.chdir(working_directory)

    # Compute execution time
    elapsed_time = (time.time() - time_on) / 60  # in minutes

    sys.stdout.write("\n")
    sys.stdout.write("You are all set!\n")
    sys.stdout.write("Navigate to project root and activate your environment with one these commands:\n")
    sys.stdout.write(f"   - For Windows CMD       : {args.venv_name}/Scripts/activate.bat\n")
    sys.stdout.write(f"   - For Windows Powershell: {args.venv_name}/Scripts/Activate.ps1\n")
    sys.stdout.write("Enjoy!\n")
    sys.stdout.write("\n")
    sys.stdout.write("Execution time: %.1f minutes.\n" % (elapsed_time))
    sys.stdout.write("\n")


# =================================================== [Execution] =================================================== #

if __name__ == "__main__":
    main()
