# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""
A Python script to automate the setup of the Python ecosystem of a project.

Prerequisites
-------------

1. This script needs to be executed at project's root.

2. Currently, this code only supports:
    * ``windows`` as operating system
    * ``poetry`` and ``flit`` as dependency management systems
    * projects without dependency management systems
    * ``poetry`` 1.2 to latest.

3. The following project structure is expected for projects without a dependency management system:
    project-name
    ├──requirements/                    # Folder containing the optional group of dependencies.
    │  ├── requirements_doc.txt         # Requirements file associated to the documentation group.
    │  ├── requirements_tests.txt       # Requirements file associated to the tests group.
    │  ├── requirements_style.txt       # Requirements file associated to the style group.
    │  └── requirements_build.txt       # Requirements file associated to the build group.

4. The following project structure is expected for projects with a dependency management system:
    project-name
    └── pyproject.toml                  # Configuration of the build system.

The following packages are needed on top of the standard Python configuration: ``toml`` and ``packaging``.

Usage
-----

To create a virtual environment and install the dependency management system of the project (if any):
    ``python setup_environment.py``

To install a particular dependency group use the ``-d`` option:
    ``python setup_environment.py -d run`` installs production dependencies
    ``python setup_environment.py -d doc`` installs doc dependencies
    ``python setup_environment.py -d tests`` installs tests dependencies
    ``python setup_environment.py -d style`` installs style dependencies
    ``python setup_environment.py -d build`` installs build dependencies

It is possible to combine several groups:
    ``python setup_environment.py -d run doc tests``

To install all available dependencies (production and optional) use the ``all`` option:
    ``python setup_environment.py -d all``

Extra dependency groups refer to any group declared in the configuration file of the dependency management system which
are not part of doc, tests, style and build. To install these groups use the ``x`` option:
    ``python setup_environment.py -x <name-of-the-group>``

There are two locations where the script will search for optional dependencies:
    * First it checks the ``pyproject.toml`` configuration file and search for optional dependency groups
    * Alternatively, it looks for a ``requirements`` folder at project root containing requirements files with the
      name of the dependency group. For instance: requirements/requirements_doc.txt for the documentation group.

To enforce the version of the dependency manager two options are possible:

    1. ``setup_environment.py`` reads the ``pyproject.toml`` and looks for a ``build-system-version`` key within
    the ``build-system-requirements`` section. The example below illustrates this. Note that,
    ``build-system-requirements` and ``build-system-version`` are not part of the ``PEP518`` standard. These syntax is
    purely internal.
    ```
    [build-system-requirements]
    build-system-version = "1.4.2"
    ```

    2. If the ``pyproject.toml`` does not contain a ``build-system-version``, the ``setup_environment.py`` checks the
    ``-s`` option which can be provided in the command line when executing the script. In the example below, version
    1.4.2 is enforced:
    ``python setup_environment.py -s 1.4.2``

Note that ``-s`` takes precedence over ``build-system-version``. If none of the two options listed above are used, the
script simply takes the latest version of the dependency manager.

To reinstall all dependencies by deleting both venvs and local poetry cache:
    ``python setup_environment.py -f``

To reinstall all dependencies by deleting venvs, local poetry cache and lock file. This option must be
used only if REALLY necessary as the installation time for the whole process will be quite long.
    ``python setup_environment.py -F``

What this script is doing?
--------------------------

The aim of this script is to automate the project installation. It creates a virtual environment, installs a
dependency manager if a configuration file is detected at project's root, configures the dependency manager to
enable package collection from private sources, installs the dependency groups following user desire.

In case ``poetry`` is detected as the project's dependency manager, two virtual environment are created. The first one
is named ``.venv`` and is located in a ``.poetry`` directory created at project's root. It is use to install
``poetry``. The second one, also named ``.venv`` is created at project's root and is controlled by ``poetry`` to
install the dependencies. This configuration is required by ``poetry``.

Future development
------------------

Given its size and its scope, this script will be refactored and transformed into a package.
"""

# ==================================================== [Imports] ==================================================== #

import argparse
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import textwrap
import time

from packaging.markers import Marker
import toml

# =================================================== [Variables] =================================================== #

SUPPORTED_DEPENDENCY_MANAGERS = {
    "poetry": {
        "configuration_file": "pyproject.toml",
        "build_backend": "poetry.core.masonry.api",
        "required_venv_name": ".venv",
        "lock_file": "poetry.lock",
        "cache_folder": ".poetry\.cache",
        "build_system_venv": ".poetry\.venv",
    },
    "flit": {
        "configuration_file": "pyproject.toml",
        "build_backend": "flit_core.buildapi",
        "required_venv_name": None,
        "lock_file": None,
        "cache_folder": ".flit/.cache",
        "build_system_venv": ".flit/.venv",
    },
}

STANDARD_OPTIONAL_DEPENDENCY_GROUPS = ["doc", "tests", "build", "style", "external"]

# =================================================== [Functions] =================================================== #

# Console prints ----------------------------------------------------------------------------------------------------


def print_main_header(text: str, max_length: int = 100) -> None:
    """Display main header."""

    for i in range(max_length):
        print("=", end="")
    print()
    print(text)
    for i in range(max_length):
        print("=", end="")
    print()
    print()


def print_section_header(text: str, max_length: int = 100) -> None:
    """Display a section header in the console."""

    section_header = ""
    if len(text) < max_length:
        section_header = text + " "
        for i in range(len(text), max_length):
            section_header += "-"
    else:
        section_header = text
    print(section_header)
    print()


def print_input_value(input: str, value: str, separator: str = ":", separator_position: int = 60) -> None:
    """Print input value in console."""

    if len(input) < separator_position:
        text = input
        for i in range(len(text), separator_position):
            text += " "
        text += separator + " " + value
    else:
        text = input + " " + separator + " " + value
    print(text)


def print_inputs_summary(args: object) -> None:
    """Display a summary of the inputs."""

    print(f"OS                                   : {platform.system()}")
    print(f"Python version                       : {get_python_version()}")
    print(f"Virtual environment name             : {args.venv_name}")
    print(f"run dependencies                     : {'yes' if 'run' in args.dependencies else 'no'}")
    for dependency_group in STANDARD_OPTIONAL_DEPENDENCY_GROUPS:
        print_input_value(
            f"{dependency_group} dependencies",
            "yes" if dependency_group in args.dependencies else "no",
            separator=":",
            separator_position=37,
        )
    if args.build_system and args.extra_dependencies:
        for dependency_group in args.extra_dependencies:
            print_input_value(
                f"{dependency_group} dependencies",
                "yes",
                separator=":",
                separator_position=37,
            )
    print(f"Dependency management system         : {args.build_system}")
    print(f"Dependency management system version : {args.build_system_version}")
    print(f"Credentials management               : {args.credentials_management_method}")
    print()


# Checks ------------------------------------------------------------------------------------------------------------


def check_dependency_management_system() -> str:
    """Check if a dependency management system is available at project root."""

    for dms_name in SUPPORTED_DEPENDENCY_MANAGERS.keys():
        if os.path.exists(SUPPORTED_DEPENDENCY_MANAGERS[dms_name]["configuration_file"]):
            dms_configuration = toml.load(SUPPORTED_DEPENDENCY_MANAGERS[dms_name]["configuration_file"])
            if (
                dms_configuration["build-system"]["build-backend"]
                == SUPPORTED_DEPENDENCY_MANAGERS[dms_name]["build_backend"]
            ):
                return dms_name


def check_virtual_environment_name(args: object) -> None:
    """Check if the virtual environment name is consistent with the build system expectations."""

    if args.build_system:
        if SUPPORTED_DEPENDENCY_MANAGERS[args.build_system]["required_venv_name"]:
            if SUPPORTED_DEPENDENCY_MANAGERS[args.build_system]["required_venv_name"] != args.venv_name:
                old_name = args.venv_name
                args.venv_name = SUPPORTED_DEPENDENCY_MANAGERS[args.build_system]["required_venv_name"]
                print(
                    f"Warning: {args.build_system} expects the name of the virtual environment name to be"
                    f" {args.venv_name}. {old_name} is replaced by {args.venv_name}."
                )


def check_python_version(args: object) -> None:
    """
    Check if the version of the current Python interpreter is consistent with the python version specifications
    from the build system.
    """

    if args.build_system:
        # Initialize lower/upper versions
        lower_version, upper_version, lower_bound_symbol, upper_bound_symbol = None, None, None, None
        lower_specification, upper_specification, single_specification = None, None, None
        # Read TOML
        configuration = toml.load(SUPPORTED_DEPENDENCY_MANAGERS[args.build_system]["configuration_file"])
        # Read Python version constraint
        python_compatibility = ""
        if args.build_system == "poetry":
            python_compatibility = configuration["tool"][args.build_system]["dependencies"]["python"].replace(" ", "")
        elif args.build_system == "flit":
            python_compatibility = configuration["project"]["requires-python"].replace(" ", "")
        # Split lower/upper version constraint
        if "," in python_compatibility:
            lower_specification, upper_specification = (
                python_compatibility.split(",")[0],
                python_compatibility.split(",")[1],
            )
        else:
            if python_compatibility.startswith(">"):
                lower_specification, upper_specification = python_compatibility, None
            elif python_compatibility.startswith("<"):
                lower_specification, upper_specification = None, python_compatibility
            else:
                single_specification = python_compatibility
        # Process lower constraint
        if lower_specification:
            lower_version = get_version_from_python_specification(lower_specification)
            lower_bound_symbol = get_sign_from_python_specification(lower_specification)
            marker = Marker(f"python_full_version {lower_bound_symbol} '{lower_version}'")
            if not marker.evaluate():
                raise Exception(f"Python version must be {lower_bound_symbol} {lower_version}.")
        # Process upper constraint
        if upper_specification:
            upper_version = get_version_from_python_specification(upper_specification)
            upper_bound_symbol = get_sign_from_python_specification(upper_specification)
            marker = Marker(f"python_full_version {upper_bound_symbol} '{upper_version}'")
            if not marker.evaluate():
                raise Exception(f"Python version must be {upper_bound_symbol} {upper_version}.")
        # Process single
        if single_specification:
            version = get_version_from_python_specification(single_specification)
            sign = get_sign_from_python_specification(single_specification)
            if sign != "==":
                raise Exception("Unable to interpret python version specification.")
            marker = Marker(f"python_full_version {sign} '{version}'")
            if not marker.evaluate():
                raise Exception(f"Python version must be equal to {version}.")


def check_existing_install(args: object) -> str:
    """Check if an install exists already."""

    return os.path.isdir(args.venv_name)


def check_inputs(args: object) -> None:
    """Check inputs consistency."""

    # Check platform
    if sys.platform != "win32":
        raise Exception("Only Windows operating systems are supported.")
    # Rework dependencies argument if all option is selected
    if "all" in args.dependencies:
        args.install_all = True
        args.dependencies = STANDARD_OPTIONAL_DEPENDENCY_GROUPS + ["run"]
    else:
        args.install_all = False
    # Check if a dependency management system is declared
    args.build_system = check_dependency_management_system()
    # Check virtual environment name
    check_virtual_environment_name(args)
    # Check python version
    check_python_version(args)
    # Check if an install already exists
    args.has_install = check_existing_install(args)


# General-purpose ---------------------------------------------------------------------------------------------------


def extract_substring_between_markers(string: str, marker_1: str, marker_2: str) -> str:
    """Extract substring between two markers using find() and slice()."""

    # find() method will search the given marker and stores its index
    mk1 = string.find(marker_1) + len(marker_1)
    # find() method will search the given marker and sotres its index
    mk2 = string.find(marker_2, mk1)
    # using slicing substring will be fetched in between markers.
    return string[mk1:mk2]


def read_integers_from_string(string: str) -> list:
    """
    Scan a string and extract integers. The regex matches any digit character (0-9).
    """

    return re.findall(r"\d+", string)


def remove_scheme_from_url(url: str) -> tuple:
    """Remove the scheme part of a URL."""

    items = url.split("://")
    if len(items) == 2:
        return items[0], items[1]
    else:
        raise Exception(f"Fail to return the URL without the scheme part for {url}.")


def get_python_version() -> None:
    """Get Python version."""

    return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"


def set_pip_command(
    package_name: str,
    package_version: str = "*",
    method: str = "install",
    pypi_url: str = "https://pypi.org/simple",
    private_pypi_token_name: str = "",
    no_deps: bool = False,
    python_executable: str = sys.executable,
) -> str:
    """Make pip command."""

    # Set command
    command = f"{python_executable} -m pip {method} {package_name}"
    # Add package version if specified
    if package_version != "*":
        command += f"=={package_version}"
    # Add part related to private PyPI source
    if pypi_url != "https://pypi.org/simple":
        # Check if token is available
        if private_pypi_token_name is None:
            raise Exception(f"No token specified for private PyPI server {pypi_url}.")
        # Check if the environment variable associated to the private PyPI token exists
        private_pypi_token = os.getenv(private_pypi_token_name)
        if private_pypi_token is None:
            raise Exception(f"Environment variable {private_pypi_token_name} does not exist.")
        # Split absolute URL
        url_scheme, relative_url = remove_scheme_from_url(pypi_url)
        # Update command line
        command += f" -i {url_scheme}://PAT:{private_pypi_token}@{relative_url}"
    # Add no-deps option
    if no_deps:
        command += " --no-deps"

    return command


def get_python_package(
    package_name: str,
    package_version: str = "*",
    method: str = "install",
    pypi_url: str = "https://pypi.org/simple",
    private_pypi_token_name: str = "",
    no_deps: bool = False,
    python_executable: str = sys.executable,
) -> None:
    """
    Install or download a python package using PIP.

    Parameters
    ----------
    package_name : str
        Name of the package.
    package_version : str
        Version of the package.
    method : str
        Get method: ``download`` or ``install``
    pypi_url : str
        URL of the PyPI server.
    private_pypi_token_name : str
        Name of the environment variable holding the token to access to the PyPI.
    python_executable : str
        Path to the Python executable.

    Returns
    -------
    None
    """

    # Set pip command
    command = set_pip_command(
        package_name=package_name,
        package_version=package_version,
        method=method,
        pypi_url=pypi_url,
        private_pypi_token_name=private_pypi_token_name,
        no_deps=no_deps,
        python_executable=python_executable,
    )
    # Run pip command
    process = subprocess.run(command.split(), check=False, shell=True, capture_output=True, text=True)
    if process.returncode != 0:
        print(process.stdout)
        print(process.stderr)
        raise Exception("Command failed with error.")


def get_python_package_versions(
    package_name: str,
    pypi_url: str = "https://pypi.org/simple",
    private_pypi_token_name: str = "",
    python_executable: str = sys.executable,
) -> None:
    """Get available versions of a package."""

    # Set pip command
    command = set_pip_command(
        package_name=package_name,
        package_version="x",
        pypi_url=pypi_url,
        private_pypi_token_name=private_pypi_token_name,
        python_executable=python_executable,
    )
    # Run pip command
    process = subprocess.run(command.split(), check=False, shell=True, capture_output=True, text=True)
    if process.returncode == 0:
        print(command)
        raise Exception("This command should have failed. There is something wrong.")
    else:
        return extract_substring_between_markers(process.stderr, "(from versions:", ")").replace(" ", "").split(",")


def upgrade_pip(python_executable: str = sys.executable) -> None:
    """Upgrade to latest PIP version in the virtual environment."""

    print("Upgrade to latest pip version")
    subprocess.run(
        [python_executable, "-m", "pip", "install", "--upgrade", "pip"],
        check=True,
        shell=True,
    )
    print()


def create_virtual_environment(args: object, venv: str = ".venv") -> None:
    """Create a virtual environment."""

    print("Create virtual environment")
    if not args.has_install or args.force_clear or args.force_clear_all:
        subprocess.run([sys.executable, "-m", "venv", venv], check=True, shell=True)
    else:
        print("Skipped")
    print()


# Dependency Management System (Build System) -----------------------------------------------------------------------


def get_private_sources(configuration_file: str) -> list:
    """Get list of private sources from configuration file."""

    configuration = toml.load(configuration_file)
    try:
        private_sources = configuration["tool"]["poetry"]["source"]
    except:
        private_sources = []
    return private_sources


def get_version_from_python_specification(specification: str) -> str:
    """Read the version."""

    return ".".join(read_integers_from_string(specification))


def get_sign_from_python_specification(specification: str) -> str:
    """Read the mathematical symbol expressing a constraint on the version."""

    first_part = specification.split(".")[0]
    sign = "".join([i for i in first_part if not i.isdigit()])
    if sign == "":
        sign = "=="
    return sign


def get_build_system_version(args: object) -> str:
    """Assign build system version."""

    if args.build_system:
        if not args.has_install or args.force_clear or args.force_clear_all:
            configuration = toml.load(SUPPORTED_DEPENDENCY_MANAGERS[args.build_system]["configuration_file"])
            if "build-system-requirements" in configuration.keys():
                if (
                    args.build_system_version == "*"
                    and "build-system-version" in configuration["build-system-requirements"]
                ):
                    args.build_system_version = configuration["build-system-requirements"]["build-system-version"]
            else:
                args.build_system_version = get_python_package_versions(args.build_system)[-1]


def install_build_system(args: object) -> None:
    """Install build system."""

    print("Install dependency management system.")
    if args.build_system:
        if not args.has_install or args.force_clear or args.force_clear_all:
            configuration = toml.load(SUPPORTED_DEPENDENCY_MANAGERS[args.build_system]["configuration_file"])
            if (
                args.build_system_version == "*"
                and "build-system-version" in configuration["build-system-requirements"]
            ):
                args.build_system_version = configuration["build-system-requirements"]["build-system-version"]
            if args.build_system == "poetry":
                create_virtual_environment(
                    args, venv=SUPPORTED_DEPENDENCY_MANAGERS[args.build_system]["build_system_venv"]
                )
                upgrade_pip(
                    python_executable=(
                        rf".\{SUPPORTED_DEPENDENCY_MANAGERS[args.build_system]['build_system_venv']}\Scripts\python"
                    )
                )
                get_python_package(
                    args.build_system,
                    args.build_system_version,
                    method="install",
                    python_executable=(
                        rf".\{SUPPORTED_DEPENDENCY_MANAGERS[args.build_system]['build_system_venv']}\Scripts\python"
                    ),
                )
            else:
                get_python_package(
                    args.build_system,
                    args.build_system_version,
                    method="install",
                    python_executable=rf".\{args.venv_name}\Scripts\python",
                    verbose=args.verbose,
                )
            print()
            # Create a file symbolic link from the virtual environment (.venv) that the build system (poetry) manages
            # to the build system executable (poetry.exe) in the poetry virtual environment (.poetry/.venv).  This
            # ensures that the correct poetry is accessible when the managed virtual environment is activated
            build_system_executable = (
                rf".\{SUPPORTED_DEPENDENCY_MANAGERS[args.build_system]['build_system_venv']}"
                rf"\Scripts\{args.build_system}.exe"
            )
            if os.path.exists(build_system_executable):
                subprocess.run(
                    [
                        "powershell",
                        "-Command",
                        "New-Item",
                        "-ItemType",
                        "SymbolicLink",
                        "-Path",
                        rf".\{args.venv_name}\Scripts\{args.build_system}.exe",
                        "-Target",
                        build_system_executable,
                    ]
                )
            return
    print("Skipped")
    print()


def configure_build_system(args: object) -> None:
    """Configure the build system to enable connection to private sources."""

    print("Configure dependency management system.")
    if args.build_system:
        if not args.has_install or args.force_clear or args.force_clear_all:
            if args.build_system == "poetry":
                configure_poetry(
                    SUPPORTED_DEPENDENCY_MANAGERS[args.build_system]["build_system_venv"],
                    args.credentials_management_method,
                )
                print()
            return
    print("Skipped")
    print()


def configure_poetry(venv_name: str, credentials_management_method: str) -> None:
    """Configure Poetry."""

    # Get list of private sources
    private_sources = get_private_sources("pyproject.toml")
    # Turn-on in-project
    subprocess.run([rf".\{venv_name}\Scripts\poetry", "config", "virtualenvs.create", "false", "--local"], check=True)
    # Turn-off virtual environment creation
    subprocess.run(
        [rf".\{venv_name}\Scripts\poetry", "config", "virtualenvs.in-project", "true", "--local"], check=True
    )
    # Turn-on poetry cache
    subprocess.run(
        [
            rf".\{venv_name}\Scripts\poetry",
            "config",
            "cache-dir",
            SUPPORTED_DEPENDENCY_MANAGERS["poetry"]["cache_folder"],
            "--local",
        ],
        check=True,
    )
    # Turn-on in-project
    subprocess.run([rf".\{venv_name}\Scripts\poetry", "config", "virtualenvs.create", "false", "--local"], check=True)
    # Declare credentials for private sources
    for source in private_sources:
        print(f"Declare credentials for {source['name']}")
        # Get source PAT
        if source["url"] == "https://pkgs.dev.azure.com/pyansys/_packaging/pyansys/pypi/simple/":
            token = os.environ["PYANSYS_PRIVATE_PYPI_PAT"]
        elif source["url"] == "https://pkgs.dev.azure.com/pyansys/_packaging/ansys-solutions/pypi/simple/":
            token = os.environ["SOLUTIONS_PRIVATE_PYPI_PAT"]
        else:
            raise Exception(f"Unknown private source {source['name']} with url {source['url']}.")
        # Store credentials
        if credentials_management_method == "keyring":
            # Declare source URL
            command_line = f"{venv_name}/Scripts/poetry config repositories.{source['name']} {source['url']} --local"
            subprocess.run(command_line, check=True)
            # Declare source credentials
            command_line = f"{venv_name}/Scripts/poetry config http-basic.{source['name']} PAT {token} --local"
            subprocess.run(command_line, check=True)
        elif credentials_management_method == "environment-variables":
            # Format source name to comply with Poetry environment variable syntax
            source_name = source["name"].upper().replace("-", "_")
            # Create Poetry environment variable
            os.environ[f"POETRY_HTTP_BASIC_{source_name}_USERNAME"] = "PAT"
            os.environ[f"POETRY_HTTP_BASIC_{source_name}_PASSWORD"] = token


def check_dependency_group(dependency_group: str, configuration: str) -> bool:
    """Return True if the dependency group is available in the configuration file."""

    try:
        configuration["tool"]["poetry"]["group"][dependency_group]
        return True
    except:
        return False


# Specifics ---------------------------------------------------------------------------------------------------------


def parser() -> None:
    """Parse command line arguments."""

    # Code Name
    program_name = "Setup Environment Utility"
    # Code description
    program_description = "A Python script to automate the setup of the Python ecosystem of a project."
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
    optional_inputs = parser.add_argument_group("Optional arguments")
    # Optional parameters
    optional_inputs.add_argument(
        "-d",
        "--dependencies",
        type=str,
        nargs="+",
        help="List of dependency groups to be installed separated by space. Example: run tests doc style build",
        default=[],
        choices=STANDARD_OPTIONAL_DEPENDENCY_GROUPS + ["run", "all"],
        required=False,
    )
    optional_inputs.add_argument(
        "-x",
        "--extra-dependencies",
        type=str,
        nargs="+",
        help="List of extra dependency groups to be installed separated by space.",
        default=[],
        required=False,
    )
    optional_inputs.add_argument(
        "-s",
        "--build-system-version",
        type=str,
        help="Build system version",
        default="*",
        required=False,
    )
    optional_inputs.add_argument(
        "-c",
        "--credentials-management-method",
        type=str,
        help="Method to store private sources credentials.",
        default="keyring",
        choices=["keyring", "environment-variables"],
        required=False,
    )
    optional_inputs.add_argument(
        "-e",
        "--venv-name",
        type=str,
        help="Name of the virtual environment. Must be '.venv' when using poetry",
        default=".venv",
        required=False,
    )
    optional_inputs.add_argument(
        "-F",
        "--force-clear-all",
        help="Clean-up the workspace. Delete existing .venv, .poetry\.venv, .poetry\.cache and poetry.lock.",
        action="store_true",
        required=False,
    )
    optional_inputs.add_argument(
        "-f",
        "--force-clear",
        help="Clean-up the workspace. Delete existing .venv., .poetry\.venv and .poetry\.cache.",
        action="store_true",
        required=False,
    )
    optional_inputs.add_argument(
        "-v",
        "--verbose",
        help="Activate verbose mode.",
        action="store_true",
        required=False,
    )

    return parser.parse_args()


def clear_workspace(args: object) -> None:
    """Remove residual items form previous installation (like venv directory, lock file ...)."""

    print("Clear workspace")
    if args.force_clear or args.force_clear_all:
        # Remove virtual environment
        if os.path.isdir(args.venv_name):
            print(f"Delete existing virtual environment {args.venv_name}.")
            shutil.rmtree(args.venv_name)
        # Remove poetry virtual environment
        if os.path.isdir(SUPPORTED_DEPENDENCY_MANAGERS[args.build_system]["build_system_venv"]):
            print("Delete existing poetry virtual environment")
            shutil.rmtree(SUPPORTED_DEPENDENCY_MANAGERS[args.build_system]["build_system_venv"])
        # Remove poetry cache
        if os.path.isdir(SUPPORTED_DEPENDENCY_MANAGERS[args.build_system]["cache_folder"]):
            print("Delete existing poetry cache")
            shutil.rmtree(SUPPORTED_DEPENDENCY_MANAGERS[args.build_system]["cache_folder"])
        if args.force_clear_all:
            # Remove lock file
            if args.build_system:
                if SUPPORTED_DEPENDENCY_MANAGERS[args.build_system]["lock_file"]:
                    if os.path.isfile(SUPPORTED_DEPENDENCY_MANAGERS[args.build_system]["lock_file"]):
                        print("Delete existing poetry lock file")
                        os.remove(SUPPORTED_DEPENDENCY_MANAGERS[args.build_system]["lock_file"])
    else:
        print("Skipped")
    print()


def install_production_dependencies(args: object) -> None:
    """Install the package (mandatory requirements only)."""

    print("Install production dependencies")
    if args.build_system and "run" in args.dependencies:
        if args.build_system == "poetry":
            subprocess.run(
                [
                    rf".\{SUPPORTED_DEPENDENCY_MANAGERS[args.build_system]['build_system_venv']}\Scripts\poetry",
                    "install",
                    "-vv",
                ],
                check=True,
                shell=True,
            )
        elif args.build_system == "flit":
            subprocess.run([rf".\{args.venv_name}\Scripts\flit", "install"], check=True, shell=True)
        print()
        return
    print("Skipped")
    print()


def install_optional_dependencies(args: object) -> None:
    """Install optional requirements (doc, tests, build or style)."""

    # Load configuration file if a dependency management system is available
    if args.build_system:
        configuration = toml.load(SUPPORTED_DEPENDENCY_MANAGERS[args.build_system]["configuration_file"])
    else:
        configuration = {}
    # Install standard optional dependency groups
    for dependency_group in STANDARD_OPTIONAL_DEPENDENCY_GROUPS:
        print(f"Install {dependency_group} dependencies")
        if dependency_group in args.dependencies:
            # Install dependency group in the configuration file of the build system
            if args.build_system:
                has_dependency_group = check_dependency_group(dependency_group, configuration)
                if has_dependency_group:
                    print("Installing from build system configuration file.")
                    subprocess.run(
                        [
                            (
                                rf".\{SUPPORTED_DEPENDENCY_MANAGERS[args.build_system]['build_system_venv']}"
                                r"\Scripts\poetry"
                            ),
                            "install",
                            "--only",
                            dependency_group,
                            "-vv",
                        ],
                        check=True,
                        shell=True,
                    )
                    print()
                    continue
            # Alternatively search dependency group in the requirements folder
            requirements_file = os.path.join("requirements", f"requirements_{dependency_group}.txt")
            if os.path.exists(requirements_file):
                print("Installing from requirements file.")
                subprocess.run(
                    [
                        rf".\{SUPPORTED_DEPENDENCY_MANAGERS[args.build_system]['build_system_venv']}\Scripts\python",
                        "-m",
                        "poetry",
                        "run",
                        "pip",
                        "install",
                        "-r",
                        requirements_file,
                        "--no-warn-conflicts",
                    ],
                    check=True,
                    shell=True,
                )
                print()
                continue
        print("Skipped")
        print()
    # Install extra optional dependency groups
    if args.build_system and args.extra_dependencies:
        for dependency_group in args.extra_dependencies:
            print(f"Install {dependency_group} dependencies")
            has_dependency_group = check_dependency_group(dependency_group, configuration)
            if has_dependency_group:
                subprocess.run(
                    [
                        rf".\{SUPPORTED_DEPENDENCY_MANAGERS[args.build_system]['build_system_venv']}\Scripts\poetry",
                        "install",
                        "--only",
                        dependency_group,
                        "-vv",
                    ],
                    check=True,
                    shell=True,
                )
            else:
                print(f"No dependency group named {dependency_group}.")
                print("Skipped")
            print()


def main() -> None:
    """Sequence of operations leading to the complete Python ecosystem."""

    # Start timer
    time_on = time.time()
    # Get current working directory
    working_directory = os.getcwd()
    # Get installation directory
    install_directory = Path(__file__).parent.absolute()
    # Move to install directory
    os.chdir(install_directory)

    # Initialize session ----------------------------------------------------------------------------------------------

    # Read command line inputs
    args = parser()

    # Check inputs consistency
    check_inputs(args)

    # Update build system version
    get_build_system_version(args)

    # Display header
    print_main_header("Setup Environment")

    # Display inputs summary
    print_inputs_summary(args)

    # Clear workspace -------------------------------------------------------------------------------------------------

    print_section_header("Clear workspace", max_length=100)

    clear_workspace(args)

    # Setup virtual environment ---------------------------------------------------------------------------------------

    print_section_header("Setup virtual environment", max_length=100)

    create_virtual_environment(args)

    upgrade_pip(python_executable=rf".\{args.venv_name}\Scripts\python")

    # Setup dependency management system ------------------------------------------------------------------------------

    print_section_header("Setup dependency management system", max_length=100)

    install_build_system(args)

    configure_build_system(args)

    # Install dependencies --------------------------------------------------------------------------------------------

    print_section_header("Install dependencies", max_length=100)

    install_production_dependencies(args)

    install_optional_dependencies(args)

    # Back to current working directory
    os.chdir(working_directory)

    # Compute execution time
    elapsed_time = (time.time() - time_on) / 60  # in minutes

    print("You are all set!")
    print("Navigate to project root and activate your environment with one these commands:")
    print(rf"   - For Windows CMD       : {args.venv_name}\Scripts\activate.bat")
    print(rf"   - For Windows Powershell: {args.venv_name}\Scripts\Activate.ps1")
    print("Enjoy!")
    print()
    print("Execution time: %.1f minutes." % (elapsed_time))
    print()


# =================================================== [Execution] =================================================== #

if __name__ == "__main__":
    main()