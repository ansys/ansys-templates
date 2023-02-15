# ©2022, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""
A Python script to automate the setup of the ecosystem of a Python project.

Usage
-----

This script needs to be executed at project's root.

To create a virtual environment and install the dependency management system of the project (if any):
    ``python setup_environment.py``

To override an existing install use the ``-f`` option to force the workspace clean-up:
    ``python setup_environment.py -f``

To select a particular version of the dependency management system use the ``-s`` option:
    ``python setup_environment.py -s 1.3``

To install the production dependencies as well as all the optional dependency groups of the project use the ``-d``
option with the keyword ``all``:
    ``python setup_environment.py -d all``

To install only a particular dependency group use ``run`` for production, ``doc`` for documentation, ``tests`` for
testing, ``style`` for code linting, and ``build`` for build. For example:
    ``python setup_environment.py -d run`` installs production dependencies
    ``python setup_environment.py -d doc`` installs doc dependencies
    ``python setup_environment.py -d tests`` installs tests dependencies
    ``python setup_environment.py -d style`` installs style dependencies
    ``python setup_environment.py -d build`` installs build dependencies

It is also possible to cummulate several groups:
    ``python setup_environment.py -d run doc tests``

Extra dependency groups refer to any group declared in the configuration file of the dependency management system which
are not part of doc, tests, style and build. To install these groups use the ``x`` option:
    ``python setup_environment.py -x <name-of-the-group>``

Currently, this code only supports:
    * ``windows`` as operating system
    * ``poetry`` and ``flit`` as dependency management systems
    * projects without dependency management systems

There are two locations where the script will search for optional dependencies:
    * First it checks the ``pyproject.toml`` configuration file and search for optional dependency groups
    * Alternatively, it looks for a ``requirements`` folder at project root containing requirements files with the
      name of the dependency group. For instance: requirements/requirements_doc.txt for the documentation group.

The following project structure is expected for projects without a dependency management system:
project-name
├──requirements/                    # Folder containing the optional group of dependencies.
│  ├── requirements_doc.txt         # Requirements file associated to the documentation group.
│  ├── requirements_tests.txt       # Requirements file associated to the tests group.
│  ├── requirements_style.txt       # Requirements file associated to the style group.
│  └── requirements_build.txt       # Requirements file associated to the build group.

The following project structure is expected for projects with a dependency management system:
project-name
└── pyproject.toml                  # Configuration of the build system.
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

supported_dependency_management_systems = {
    "poetry": {
        "configuration_file": "pyproject.toml",
        "build_backend": "poetry.core.masonry.api",
        "required_venv_name": ".venv",
        "lock_file": "poetry.lock",
    },
    "flit": {
        "configuration_file": "pyproject.toml",
        "build_backend": "flit_core.buildapi",
        "required_venv_name": None,
        "lock_file": None,
    },
}

standard_optional_dependency_groups = ["doc", "tests", "build", "style"]

# =================================================== [Functions] =================================================== #

# Console prints ----------------------------------------------------------------------------------------------------


def print_main_header(text, max_lenght=100):
    """Display main header."""

    for i in range(max_lenght):
        print("=", end="")
    print()
    print(text)
    for i in range(max_lenght):
        print("=", end="")
    print()
    print()


def print_section_header(text, max_lenght=100):
    """Display a section header in the console."""
    section_header = ""
    if len(text) < max_lenght:
        section_header = text + " "
        for i in range(len(text), max_lenght):
            section_header += "-"
    else:
        section_header = text
    print(section_header)
    print()


def print_input_value(input, value, separator=":", separator_position=60):
    """Print input value in console."""
    if len(input) < separator_position:
        text = input
        for i in range(len(text), separator_position):
            text += " "
        text += separator + " " + value
    else:
        text = input + " " + separator + " " + value
    print(text)


def print_inputs_summary(args):
    """Display a summary of the inputs."""

    print("OS                                   : %s" % (platform.system()))
    print("Python version                       : %s" % (get_python_version()))
    print("Virtual environment name             : %s" % (args.venv_name))
    print("run dependencies                     : %s" % ("yes" if "run" in args.dependencies else "no"))
    for dependency_group in standard_optional_dependency_groups:
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
    print("Dependency management system         : %s" % (args.build_system))
    print("Dependency management system version : %s" % (args.build_system_version))
    print("Credentials management               : %s" % (args.credentials_management_method))
    print("")


# Checks ------------------------------------------------------------------------------------------------------------


def check_dependency_management_system():
    """Check if a dependency management system is available at project root."""
    for dms_name in supported_dependency_management_systems.keys():
        if os.path.exists(supported_dependency_management_systems[dms_name]["configuration_file"]):
            dms_configuration = toml.load(supported_dependency_management_systems[dms_name]["configuration_file"])
            if (
                dms_configuration["build-system"]["build-backend"]
                == supported_dependency_management_systems[dms_name]["build_backend"]
            ):
                return dms_name


def check_virtual_environment_name(args):
    """Check if the virtual environment name is consistent with the build system expectations."""
    if args.build_system:
        if supported_dependency_management_systems[args.build_system]["required_venv_name"]:
            if supported_dependency_management_systems[args.build_system]["required_venv_name"] != args.venv_name:
                old_name = args.venv_name
                args.venv_name = supported_dependency_management_systems[args.build_system]["required_venv_name"]
                print(
                    f"Warning: {args.build_system} expects the name of the virtual environment name to be "
                    f"{args.venv_name}. {old_name} is replaced by {args.venv_name}."
                )


def check_python_version(args):
    """
    Check if the version of the current Python interpreter is consistent with the python version specifications
    from the build system.
    """
    if args.build_system:
        # Initialize lower/upper versions
        lower_version, upper_version, lower_sign, upper_sign = None, None, None, None
        lower_specification, upper_specification, single_specification = None, None, None
        # Read TOML
        configuration = toml.load(supported_dependency_management_systems[args.build_system]["configuration_file"])
        # Read Python version constraint
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
            lower_sign = get_sign_from_python_specification(lower_specification)
            marker = Marker(f"python_full_version {lower_sign} '{lower_version}'")
            if not marker.evaluate():
                raise Exception(f"Python version must be greater than or equal to {lower_version}.")
        # Process upper constraint
        if upper_specification:
            upper_version = get_version_from_python_specification(upper_specification)
            upper_sign = get_sign_from_python_specification(upper_specification)
            marker = Marker(f"python_full_version {upper_sign} '{upper_version}'")
            if not marker.evaluate():
                raise Exception(f"Python version must be lower than or equal to {upper_version}.")
        # Process single
        if single_specification:
            version = get_version_from_python_specification(single_specification)
            sign = get_sign_from_python_specification(single_specification)
            if sign != "==":
                raise Exception("Unable to interpret python version specification.")
            marker = Marker(f"python_full_version {sign} '{version}'")
            if not marker.evaluate():
                raise Exception(f"Python version must be equal to {version}.")


def check_existing_install(args):
    """Check if an install exists already."""
    if os.path.isdir(args.venv_name):
        return True


def check_inputs(args):
    """Check inputs consistency."""
    # Check platform
    if sys.platform != "win32":
        raise Exception("Only Windows operating systems are supported.")
    # Rework dependencies argument if all option is selected
    if "all" in args.dependencies:
        args.install_all = True
        args.dependencies = standard_optional_dependency_groups + ["run"]
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


def read_integers_from_string(string):
    """
    Scan a string and extract integers.

    The regex matches any digit character (0-9).
    """
    return re.findall("\d+", string)


def remove_scheme_from_url(url):
    """Remove the scheme part of a URL."""
    items = url.split("://")
    if len(items) == 2:
        return items[0], items[1]
    else:
        raise Exception(f"Fail to return the URL without the scheme part for {url}.")


def get_python_version():
    """Get Python version."""
    return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"


def get_python_package(
    package_name: str,
    package_version: str = "*",
    method: str = "install",
    pypi_url: str = "https://pypi.org/simple",
    private_pypi_token_name: str = None,
    no_deps: bool = False,
    python_executable: str = sys.executable,
    verbose: bool = True,
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
        if os.environ.get(private_pypi_token_name) is None:
            raise Exception("Environment variable {private_pypi_token_name} does not exist.")
        # Get private PyPI token
        private_pypi_token = os.environ[private_pypi_token_name]
        # Split absolute URL
        url_scheme, relative_url = remove_scheme_from_url(pypi_url)
        # Update command line
        command += f" -i {url_scheme}://PAT:{private_pypi_token}@{relative_url}"
    # Add no-deps option
    if no_deps:
        command += " --no-deps"
    # Run command with dummy version to force PIP to return the list of released versions
    returncode, stdout, stderr = run_command(command, display_output=verbose)
    if returncode != 0:
        print(stdout)
        raise Exception("Command failed with error.")


def run_command(cmd, display_output=True):
    """
    Run command.
    """
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if display_output:
        stdout, stderr = b"", b""
        for line in process.stdout:
            sys.stdout.buffer.write(line)
            sys.stdout.buffer.flush()
            stdout += line
        process.wait()
    else:
        stdout, stderr = process.communicate()

    if isinstance(stdout, bytes):
        try:
            stdout = stdout.decode().splitlines()
        except:
            raise Exception("Unable to decode stdout.")

    if isinstance(stderr, bytes):
        try:
            stderr = stderr.decode().splitlines()
        except:
            raise Exception("Unable to decode stderr.")

    return process.returncode, stdout, stderr


def upgrade_pip(python_executable: str = sys.executable) -> None:
    """Upgrade to latest PIP version"""
    print("Upgrade to latest pip version")
    subprocess.run(
        [python_executable, "-m", "pip", "install", "--upgrade", "pip"],
        check=True,
        shell=True,
    )
    print()


def create_virtual_environment(args):
    """Create a virtual environment."""

    print("Create virtual environment")
    if not args.has_install or args.force_clear:
        subprocess.run([sys.executable, "-m", "venv", ".venv"])
    else:
        print("Skipped")
    print()


# Dependency Management System (Build System) -----------------------------------------------------------------------


def get_private_sources(configuration_file):
    """Get list of private sources from configuration file."""
    configuration = toml.load(configuration_file)
    try:
        private_sources = configuration["tool"]["poetry"]["source"]
    except:
        private_sources = []
    return private_sources


def get_version_from_python_specification(specification):
    """Read the version."""
    return ".".join(read_integers_from_string(specification))


def get_sign_from_python_specification(specification):
    """Read the mathematical symbol expressing a constraint on the version."""
    first_part = specification.split(".")[0]
    sign = "".join([i for i in first_part if not i.isdigit()])
    if sign == "":
        sign = "=="
    return sign


def install_build_system(args):
    """Install build system."""
    print(f"Install dependency management system.")
    if args.build_system:
        if not args.has_install or args.force_clear:
            get_python_package(
                args.build_system,
                args.build_system_version,
                method="install",
                python_executable=rf".\{args.venv_name}\Scripts\python",
                verbose=args.verbose,
            )
            print()
            return
    print("Skipped")
    print()


def configure_build_system(args):
    """Configure the build system to enable connection to private sources."""
    print(f"Configure dependency management system.")
    if args.build_system:
        if not args.has_install or args.force_clear:
            if args.build_system == "poetry":
                configure_poetry(args.venv_name, args.credentials_management_method)
                print()
            return
    print("Skipped")
    print()


def configure_poetry(venv_name, credentials_management_method):
    """Configure Poetry."""
    # Turn-on in-project
    subprocess.run([rf".\{venv_name}\Scripts\poetry", "config", "virtualenvs.in-project", "true"])
    # Get list of private sources
    private_sources = get_private_sources("pyproject.toml")
    # Delete existing configuration
    print("Clean-up existing poetry configurations")
    if sys.platform == "win32":
        username = os.getlogin()
        path_poetry_config = r"C:\Users\%s\AppData\Roaming\pypoetry" % (username)
        if os.path.isfile(os.path.join(path_poetry_config, "config.toml")):
            os.remove(os.path.join(path_poetry_config, "config.toml"))
        if os.path.isfile(os.path.join(path_poetry_config, "auth.toml")):
            os.remove(os.path.join(path_poetry_config, "auth.toml"))
    # Declare credentials for private sources
    for source in private_sources:
        print("Declare credentials for %s" % (source["name"]))
        # Get source PAT
        if source["url"] == "https://pkgs.dev.azure.com/pyansys/_packaging/pyansys/pypi/simple/":
            token = os.environ["PYANSYS_PRIVATE_PYPI_PAT"]
        elif source["url"] == "https://pkgs.dev.azure.com/pyansys/_packaging/ansys-solutions/pypi/simple/":
            token = os.environ["SOLUTIONS_PRIVATE_PYPI_PAT"]
        else:
            raise Exception("Unknown private source %s with url %s." % (source["name"], source["url"]))
        # Store credentials
        if credentials_management_method == "keyring":
            # Declare source URL
            command_line = "%s/Scripts/poetry config repositories.%s %s" % (venv_name, source["name"], source["url"])
            subprocess.run(command_line, check=True)
            # Declare source credentials
            command_line = "%s/Scripts/poetry config http-basic.%s PAT %s" % (venv_name, source["name"], token)
            subprocess.run(command_line, check=True)
        elif credentials_management_method == "environment-variables":
            # Format source name to comply with Poetry environment variable syntax
            source_name = source["name"].upper().replace("-", "_")
            # Create Poetry environment variable
            os.environ[f"POETRY_HTTP_BASIC_{source_name}_USERNAME"] = "PAT"
            os.environ[f"POETRY_HTTP_BASIC_{source_name}_PASSWORD"] = token


def check_dependency_group(dependency_group, configuration):
    """Return True if the dependency group is available in the configuration file."""
    try:
        configuration["tool"]["poetry"]["group"][dependency_group]
        return True
    except:
        return False


# Specifics ---------------------------------------------------------------------------------------------------------


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
        help="List of dependency groups to be installed separated by space. Example: run tests doc style build",
        default=[],
        choices=standard_optional_dependency_groups + ["run", "all"],
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
        help="Name of the virtual environment.",
        default=".venv",
        required=False,
    )
    optional_inputs.add_argument(
        "-f",
        "--force-clear",
        help="Clean-up the workspace. Delete existing .venv and poetry.lock.",
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


def clear_workspace(args):
    """Remove residual items form previous installation (like venv directory, lock file ...)."""
    print("Clear workspace")
    if args.force_clear:
        # Remove virtual environment
        if os.path.isdir(args.venv_name):
            print(f"Delete existing virtual environment {args.venv_name}.")
            shutil.rmtree(args.venv_name)
        # Remove lock file
        if args.build_system:
            if supported_dependency_management_systems[args.build_system]["lock_file"]:
                if os.path.isfile(supported_dependency_management_systems[args.build_system]["lock_file"]):
                    print("Delete existing poetry lock file")
                    os.remove(supported_dependency_management_systems[args.build_system]["lock_file"])
    else:
        print("Skipped")
    print("")


def install_production_dependencies(args):
    """Install the package (mandatory requirements only)."""
    print(f"Install production dependencies")
    if args.build_system and "run" in args.dependencies:
        if args.build_system == "poetry":
            subprocess.run(
                [rf".\{args.venv_name}\Scripts\poetry", "install", "--only", "main", "-vv"], check=True, shell=True
            )
        elif args.build_system == "flit":
            subprocess.run([rf".\{args.venv_name}\Scripts\flit", "install"], check=True, shell=True)
        print()
        return
    print("Skipped")
    print()


def install_optional_dependencies(args):
    """Install optional requirements (doc, tests, build or style)."""
    # Load configuration file if a dependency management system is available
    if args.build_system:
        configuration = toml.load(supported_dependency_management_systems[args.build_system]["configuration_file"])
    # Install standard optional dependency groups
    for dependency_group in standard_optional_dependency_groups:
        print("Install %s dependencies" % (dependency_group))
        if dependency_group in args.dependencies:
            # Install dependency group in the configuration file of the build system
            if args.build_system:
                has_dependency_group = check_dependency_group(dependency_group, configuration)
                if has_dependency_group:
                    print("Installing from build system configuration file.")
                    subprocess.run(
                        [rf".\{args.venv_name}\Scripts\poetry", "install", "--only", dependency_group, "-vv"],
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
                        rf".\{args.venv_name}\Scripts\python",
                        "-m",
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
            print("Install %s dependencies" % (dependency_group))
            has_dependency_group = check_dependency_group(dependency_group, configuration)
            if has_dependency_group:
                subprocess.run(
                    [rf".\{args.venv_name}\Scripts\poetry", "install", "--only", dependency_group, "-vv"],
                    check=True,
                    shell=True,
                )
            else:
                print(f"No dependency group named {dependency_group}.")
                print("Skipped")
            print()


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

    # Initialize session ----------------------------------------------------------------------------------------------

    # Read command line inputs
    args = parser()

    # Check inputs consistency
    check_inputs(args)

    # Display header
    print_main_header("Setup Environment")

    # Display inputs summary
    print_inputs_summary(args)

    # Clear workspace -------------------------------------------------------------------------------------------------

    print_section_header("Clear workspace", max_lenght=100)

    clear_workspace(args)

    # Setup virtual environment ---------------------------------------------------------------------------------------

    print_section_header("Setup virtual environment", max_lenght=100)

    create_virtual_environment(args)

    upgrade_pip(python_executable=rf".\{args.venv_name}\Scripts\python")

    # Setup dependency management system ------------------------------------------------------------------------------

    print_section_header("Setup dependency management system", max_lenght=100)

    install_build_system(args)

    configure_build_system(args)

    # Install dependencies --------------------------------------------------------------------------------------------

    print_section_header("Install dependencies", max_lenght=100)

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
    print("")
    print("Execution time: %.1f minutes." % (elapsed_time))
    print("")


# =================================================== [Execution] =================================================== #

if __name__ == "__main__":
    main()
