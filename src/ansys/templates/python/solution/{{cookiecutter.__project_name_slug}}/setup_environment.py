# ©2023, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""
A Python script to automate the setup of the Python ecosystem of a project.

Prerequisites
-------------

1. The following packages are required:
    * packaging
    * toml

2. This script needs to be executed at project's root.

Usage
-----

To create a virtual environment and install the dependency management system of the project:
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

To enforce the version of the dependency manager two options are possible:

    1. ``setup_environment.py`` reads the ``pyproject.toml`` and looks for a ``build-system-version`` key within
    the ``build-system-requirements`` section. The example below illustrates this. Note that,
    ``build-system-requirements` and ``build-system-version`` are not part of the ``PEP518`` standard. These syntax is
    purely internal.
    ```
    [build-system-requirements]
    build-system-version = "1.8.4"
    ```

    2. If the ``pyproject.toml`` does not contain a ``build-system-version``, the ``setup_environment.py`` checks the
    ``-s`` option which can be provided in the command line when executing the script. In the example below, version
    1.8.4 is enforced:
    ``python setup_environment.py -s 1.8.4``

Note that ``-s`` takes precedence over ``build-system-version``. If none of the two options listed above are used, the
script simply takes the latest version of the dependency manager.

To reinstall all dependencies by deleting both venvs and local poetry cache:
    ``python setup_environment.py -f``

To reinstall all dependencies by deleting venvs, local poetry cache and lock file. This option must be
used only if REALLY necessary as the installation time for the whole process will be quite long.
    ``python setup_environment.py -F``

Private sources
---------------

If a private source is declared in the pyproject.toml file, the script expects the credentials to be stored in
environment variables and declared in the .env file at project's root. Given a private source declared in the
pyproject.toml under the named ``my-private-pypi``, the following environment variables must be declared in the
.env file:
    * MY_PRIVATE_PYPI_USERNAME: the username associated with the private source.
    * MY_PRIVATE_PYPI_PASSWORD: the download token of the private source.

If a custom certificate authority is required to access the private source, the following environment variable
must be declared:
    * MY_PRIVATE_PYPI_CERTIFICATE: the path to the certificate authority file.

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

if platform.system() == "Windows":
    import winreg

try:
    from packaging.markers import Marker
except:
    sys.exit("Process stopped. The `packaging` library is missing. Install with: `pip install packaging`.")
try:
    import toml
except:
    sys.exit("Process stopped. The `toml` library is missing. Install with: `pip install toml`.")

# =================================================== [Variables] =================================================== #

DEPENDENCY_MANAGER_PATHS = {
    "win32": {
        "poetry_python_executable": Path(".poetry").absolute() / ".venv" / "Scripts" / "python.exe",
        "build_sys_exec": Path(".poetry").absolute() / ".venv" / "Scripts" / "poetry.exe",
        "dep_bin_venv_path": Path(".venv").absolute() / "Scripts" / "poetry.exe",
        "python_executable": Path(".venv").absolute() / "Scripts" / "python.exe",
        "shell": True,
    },
    "linux": {
        "poetry_python_executable": Path(".poetry").absolute() / ".venv" / "bin" / "python",
        "build_sys_exec": Path(".poetry").absolute() / ".venv" / "bin" / "poetry",
        "dep_bin_venv_path": Path(".venv").absolute() / "bin" / "poetry",
        "python_executable": Path(".venv").absolute() / "bin" / "python",
        "shell": False,
    },
    "common": {
        "configuration_file": "pyproject.toml",
        "build_backend": "poetry.core.masonry.api",
        "required_venv_name": ".venv",
        "lock_file": "poetry.lock",
        "build_system_venv": Path(".poetry") / ".venv",
        "cache_folder": Path(".poetry").absolute() / ".cache",
    },
}

configuration = toml.load(DEPENDENCY_MANAGER_PATHS["common"]["configuration_file"])
STANDARD_OPTIONAL_DEPENDENCY_GROUPS = []
if "group" in configuration["tool"]["poetry"].keys():
    if len(configuration["tool"]["poetry"]["group"].keys()):
        STANDARD_OPTIONAL_DEPENDENCY_GROUPS = [group for group in configuration["tool"]["poetry"]["group"].keys()]

# =================================================== [Functions] =================================================== #

# Console prints ----------------------------------------------------------------------------------------------------


def print_main_header(text: str, max_length: int = 100) -> None:
    """Display main header."""
    for _ in range(max_length):
        print("=", end="")
    print()
    print(text)
    for _ in range(max_length):
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
    if args.extra_dependencies:
        for dependency_group in args.extra_dependencies:
            print_input_value(
                f"{dependency_group} dependencies",
                "yes",
                separator=":",
                separator_position=37,
            )
    print("Dependency management system         : poetry")
    print(f"Dependency management system version : {args.build_system_version}")
    print(f"Credentials management               : {args.credentials_management_method}")
    print()


# Checks ------------------------------------------------------------------------------------------------------------


def check_virtual_environment_name(args: object) -> None:
    """Check if the virtual environment name is consistent with the build system expectations."""
    if DEPENDENCY_MANAGER_PATHS["common"]["required_venv_name"] != args.venv_name:
        old_name = args.venv_name
        args.venv_name = DEPENDENCY_MANAGER_PATHS["common"]["required_venv_name"]
        print(
            f"Warning: poetry expects the name of the virtual environment name to be"
            f" {args.venv_name}. {old_name} is replaced by {args.venv_name}."
        )


def check_python_version(args: object) -> None:
    """Check if current Python is consistent with the python specifications from the build system."""
    # Initialize lower/upper versions
    lower_version, upper_version, lower_bound_symbol, upper_bound_symbol = None, None, None, None
    lower_specification, upper_specification, single_specification = None, None, None
    # Read TOML
    configuration = toml.load(DEPENDENCY_MANAGER_PATHS["common"]["configuration_file"])
    # Read Python version constraint
    python_compatibility = configuration["tool"]["poetry"]["dependencies"]["python"].replace(" ", "")
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

    if single_specification:
        version = get_version_from_python_specification(single_specification)
        sign = get_sign_from_python_specification(single_specification)
        if sign != "==":
            raise Exception("Unable to interpret python version specification.")
        marker = Marker(f"python_full_version {sign} '{version}'")
        if not marker.evaluate():
            raise Exception(f"Python version must be equal to {version}.")
    else:
        error_message = "Python version must be "
        if lower_specification:
            lower_version = get_version_from_python_specification(lower_specification)
            lower_bound_symbol = get_sign_from_python_specification(lower_specification)
            lower_marker = Marker(f"python_full_version {lower_bound_symbol} '{lower_version}'")
            error_message += f"{lower_bound_symbol} {lower_version}"
        if upper_specification:
            upper_version = get_version_from_python_specification(upper_specification)
            upper_bound_symbol = get_sign_from_python_specification(upper_specification)
            upper_marker = Marker(f"python_full_version {upper_bound_symbol} '{upper_version}'")
            if lower_specification:
                error_message += f" and "
            error_message += f"{upper_bound_symbol} {upper_version}"
        if lower_specification:
            if not lower_marker.evaluate():
                raise Exception(error_message)
        if upper_specification:
            if not upper_marker.evaluate():
                raise Exception(error_message)


def check_existing_install(args: object) -> str:
    """Check if an install exists already."""
    return os.path.isdir(args.venv_name)


def is_long_paths_enabled():
    """Check if long paths are enabled on Windows."""
    try:
        # Open the registry key
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\FileSystem") as key:
            # Read the value of LongPathsEnabled
            value, _ = winreg.QueryValueEx(key, "LongPathsEnabled")
            return value == 1
    except FileNotFoundError:
        # The key doesn't exist, which means long paths are not enabled
        return False


def is_path_too_long(path):
    """Check if the path exceeds the maximum allowed length on Windows."""
    # Maximum allowed path length for Windows
    max_path_length_windows = 260

    # Check if the path to each file is too long
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            if len(file_path) > max_path_length_windows:
                return True
    return False


def check_inputs(args: object) -> None:
    """Check inputs consistency."""
    # Rework dependencies argument if all option is selected
    if "all" in args.dependencies:
        args.install_all = True
        args.dependencies = STANDARD_OPTIONAL_DEPENDENCY_GROUPS + ["run"]
    else:
        args.install_all = False

    # Check virtual environment name
    check_virtual_environment_name(args)
    # Check python version
    check_python_version(args)
    # Check if an install already exists
    args.has_install = check_existing_install(args)

    if args.local_wheels:
        if not os.path.exists(args.local_wheels):
            raise FileNotFoundError(f"The directory '{args.local_wheels}' does not exist.")

        if sys.platform == "win32":
            path_too_long = is_path_too_long(args.local_wheels)

            if path_too_long and not is_long_paths_enabled():
                raise Exception(
                    f"Path length to file(s) in '{args.local_wheels}' exceeds the maximum limit in Windows."
                    "Please enable Windows Long Path support or use a shorter path. You can find information on "
                    "how to enable this at https://pip.pypa.io/warnings/enable-long-paths"
                )

    private_sources = get_private_sources("pyproject.toml")
    for source in private_sources:
        if source["name"].lower() == "pypi":
            continue
        token_environment_variable = source["name"].upper().replace("-", "_") + "_TOKEN"
        token = os.getenv(token_environment_variable, None)
        if token:
            url_scheme, relative_url = remove_scheme_from_url(source["url"])
            command = [
                sys.executable,
                "-m",
                "pip",
                "install",
                "ansys-saf-glow-engine==x",
                "-i",
                f"{url_scheme}://{token}@{relative_url}",
            ]

            process = subprocess.run(
                command,
                check=False,
                shell=DEPENDENCY_MANAGER_PATHS[sys.platform]["shell"],
                capture_output=True,
                text=True,
            )
            if process.returncode != 0:
                if "401 Error, Credentials not correct" in str(process.stderr):
                    raise Exception(
                        f"Token for {source['name']} is incorrect. "
                        "Please set the correct token in the environment variable {token_environment_variable}."
                    )
        else:
            raise Exception(
                f"Token for {source['name']} is missing. "
                "Please set the environment variable {token_environment_variable} with the token."
            )


def modify_toml_file_in_case_of_wheel_files(args: object) -> None:
    """Modify the toml file in case of wheel files."""
    if not args.local_wheels:
        return

    wheels_path = args.local_wheels
    wheel_files = {
        filename.split("-")[0].replace("_", "-"): os.path.join(wheels_path, filename)
        for filename in os.listdir(wheels_path)
    }

    # Add the local wheels to the toml file
    configuration = toml.load(DEPENDENCY_MANAGER_PATHS["common"]["configuration_file"])
    check_that_all_wheels_are_provided(wheel_files=wheel_files, configuration=configuration)

    for package_name, wheel_file in wheel_files.items():
        if package_name in configuration["tool"]["poetry"]["dependencies"]:
            del configuration["tool"]["poetry"]["dependencies"][package_name]
        configuration["tool"]["poetry"]["dependencies"][package_name] = {"file": wheel_file}

    with open(os.path.join(os.getcwd(), DEPENDENCY_MANAGER_PATHS["common"]["configuration_file"]), "w") as f:
        toml.dump(configuration, f)


def check_that_all_wheels_are_provided(wheel_files: dict, configuration: dict) -> None:
    """Check that all wheels are provided in the local wheels directory."""
    private_packages = find_private_packages_in_lock_file()

    for private_package in private_packages:
        wheel_is_found = private_package in wheel_files
        if not wheel_is_found:
            raise FileNotFoundError(f"{private_package}.whl cannot be found in the local python wheels directory")


def find_private_packages_in_lock_file() -> list:
    """Find private packages in the lock file."""
    lock_data = toml.load(os.path.join(os.getcwd(), DEPENDENCY_MANAGER_PATHS["common"]["lock_file"]))
    packages = lock_data.get("package", [])

    private_packages = [
        package["name"]
        for package in packages
        if package.get("source", {}).get("reference") == "solutions-private-pypi"
    ]

    return private_packages


# General-purpose ---------------------------------------------------------------------------------------------------


def extract_substring_between_markers(string: str, marker_1: str, marker_2: str) -> str:
    """Extract substring between two markers using find() and slice()."""
    # find() method will search the given marker and stores its index
    mk1 = string.find(marker_1) + len(marker_1)
    # find() method will search the given marker and stores its index
    mk2 = string.find(marker_2, mk1)
    # using slicing substring will be fetched in between markers.
    return string[mk1:mk2]


def read_integers_from_string(string: str) -> list:
    """Scan a string and extract integers. The regex matches any digit character (0-9)."""
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
    package_version: str = "*",
    method: str = "install",
    pypi_url: str = "https://pypi.org/simple",
    private_pypi_token_name: str = "",
    no_deps: bool = False,
    python_executable: str = sys.executable,
) -> str:
    """Make pip command."""
    package_name = "poetry"

    # Add package version if specified
    if package_version != "*":
        package_name += f"=={package_version}"
    # Set command
    command = [python_executable, "-m", "pip", method, package_name]
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
        package_version=package_version,
        method=method,
        pypi_url=pypi_url,
        private_pypi_token_name=private_pypi_token_name,
        no_deps=no_deps,
        python_executable=python_executable,
    )
    # Run pip command
    process = subprocess.run(
        command, check=False, shell=DEPENDENCY_MANAGER_PATHS[sys.platform]["shell"], capture_output=True, text=True
    )
    if process.returncode != 0:
        print(process.stdout)
        print(process.stderr)
        raise Exception("Command failed with error.")


def get_python_package_versions(
    pypi_url: str = "https://pypi.org/simple",
    private_pypi_token_name: str = "",
    python_executable: str = sys.executable,
) -> None:
    """Get available versions of a package."""
    # Set pip command
    command = set_pip_command(
        package_version="x",
        pypi_url=pypi_url,
        private_pypi_token_name=private_pypi_token_name,
        python_executable=python_executable,
    )
    # Run pip command
    process = subprocess.run(
        command, check=False, shell=DEPENDENCY_MANAGER_PATHS[sys.platform]["shell"], capture_output=True, text=True
    )
    if process.returncode == 0:
        print(command)
        raise Exception("This command should have failed. There is something wrong.")
    else:
        return extract_substring_between_markers(process.stderr, "(from versions:", ")").replace(" ", "").split(",")


def create_virtual_environment(args: object, venv: str = ".venv") -> None:
    """Create a virtual environment."""
    print("Create virtual environment")
    if not args.has_install or args.force_clear or args.force_clear_all:
        if sys.platform == "linux":
            subprocess.run([sys.executable, "-m", "pip", "install", "virtualenv"], check=True)
        subprocess.run(
            [sys.executable, "-m", "venv", venv], check=True, shell=DEPENDENCY_MANAGER_PATHS[sys.platform]["shell"]
        )
    else:
        print("Skipped")
    print()


def load_env_file(file_path):
    """Load content of an environment file into the environment variables."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} does not exist.")

    var_pattern = re.compile(r"\$\{(\w+)\}")

    def resolve_value(value):
        """Resolve environment variable placeholders in the value."""
        matches = var_pattern.findall(value)
        for match in matches:
            env_value = os.getenv(match, "")
            value = value.replace(f"${{{match}}}", env_value)
        return value

    with open(file_path) as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, value = line.split("=", 1)
                resolved_value = resolve_value(value.strip())
                os.environ[key.strip()] = resolved_value


def is_virtual_environment():
    """Check if the current Python environment is a virtual environment."""
    return sys.prefix != sys.base_prefix


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
    if not args.has_install or args.force_clear or args.force_clear_all:
        configuration = toml.load(DEPENDENCY_MANAGER_PATHS["common"]["configuration_file"])
        if "build-system-requirements" in configuration.keys():
            if (
                args.build_system_version == "*"
                and "build-system-version" in configuration["build-system-requirements"]
            ):
                args.build_system_version = configuration["build-system-requirements"]["build-system-version"]
        else:
            args.build_system_version = get_python_package_versions()[-1]


def install_build_system(args: object) -> None:
    """Install build system."""
    print("Install dependency management system.")
    if not args.has_install or args.force_clear or args.force_clear_all:
        configuration = toml.load(DEPENDENCY_MANAGER_PATHS["common"]["configuration_file"])
        if args.build_system_version == "*" and "build-system-version" in configuration["build-system-requirements"]:
            args.build_system_version = configuration["build-system-requirements"]["build-system-version"]

        create_virtual_environment(args, venv=DEPENDENCY_MANAGER_PATHS["common"]["build_system_venv"])
        get_python_package(
            args.build_system_version,
            method="install",
            python_executable=DEPENDENCY_MANAGER_PATHS[sys.platform]["poetry_python_executable"],
        )
        print()
        # Create a file symbolic link from the virtual environment (.venv) that the build system (poetry) manages
        # to the build system executable (poetry.exe) in the poetry virtual environment (.poetry/.venv).  This
        # ensures that the correct poetry is accessible when the managed virtual environment is activated
        build_system_executable = DEPENDENCY_MANAGER_PATHS[sys.platform]["build_sys_exec"]
        if os.path.exists(build_system_executable):
            if sys.platform == "win32":
                subprocess.run(
                    [
                        "powershell",
                        "-Command",
                        "New-Item",
                        "-ItemType",
                        "HardLink",
                        "-Path",
                        f"'{DEPENDENCY_MANAGER_PATHS[sys.platform]['dep_bin_venv_path']}'",
                        "-Target",
                        f"'{build_system_executable}'",
                    ]
                )
            elif sys.platform == "linux":
                subprocess.run(
                    [
                        "ln",
                        "-sf",
                        build_system_executable,
                        DEPENDENCY_MANAGER_PATHS[sys.platform]["dep_bin_venv_path"],
                    ]
                )
        return
    print("Skipped")
    print()


def configure_build_system(args: object) -> None:
    """Configure the build system to enable connection to private sources."""
    print("Configure dependency management system.")
    if not args.has_install or args.force_clear or args.force_clear_all:
        configure_poetry(
            DEPENDENCY_MANAGER_PATHS["common"]["build_system_venv"],
            args.credentials_management_method,
            modern_installation=not args.disable_modern_installation,
            use_private_sources=not bool(args.local_wheels),
        )
        print()
        return
    print("Skipped")
    print()


def configure_poetry(
    venv_name: str,
    credentials_management_method: str,
    modern_installation: bool = True,
    use_private_sources: bool = True,
) -> None:
    """Configure Poetry."""
    poetry_executable = DEPENDENCY_MANAGER_PATHS[sys.platform]["dep_bin_venv_path"]
    # Get list of private sources
    private_sources = get_private_sources("pyproject.toml")
    # Turn-on in-project
    subprocess.run([poetry_executable, "config", "virtualenvs.create", "false", "--local"], check=True)
    # Turn-off virtual environment creation
    subprocess.run([poetry_executable, "config", "virtualenvs.in-project", "true", "--local"], check=True)
    # Turn-on poetry cache
    subprocess.run(
        [
            poetry_executable,
            "config",
            "cache-dir",
            DEPENDENCY_MANAGER_PATHS["common"]["cache_folder"],
            "--local",
        ],
        check=True,
    )
    # Turn-on in-project
    subprocess.run([poetry_executable, "config", "virtualenvs.create", "false", "--local"], check=True)
    # Turn-off modern-installation
    if not modern_installation:
        subprocess.run([poetry_executable, "config", "installer.modern-installation", "false", "--local"], check=True)

    if not use_private_sources:
        return

    # Declare credentials for private sources
    for source in private_sources:
        if source["name"].lower() == "pypi":
            continue
        print(f"Declare credentials for {source['name']}")
        source_name_slug = source["name"].upper().replace("-", "_")
        username = os.environ.get(f"{source_name_slug}_USERNAME", "")
        token = os.environ.get(f"{source_name_slug}_TOKEN", None)
        if not token:
            raise Exception(f"No token found for private source {source['url']}.")
        certificate = os.environ.get(f"{source_name_slug}_CERTIFICATE", None)

        # Store credentials
        if credentials_management_method == "keyring":
            # Declare source URL
            command_line = [poetry_executable, "config", f"repositories.{source['name']}", source["url"], "--local"]
            subprocess.run(command_line, check=True)
            # Declare source credentials
            command_line = [poetry_executable, "config", f"http-basic.{source['name']}", username, token, "--local"]
            subprocess.run(command_line, check=True)
        elif credentials_management_method == "environment-variables":
            # Format source name to comply with Poetry environment variable syntax
            source_name = source["name"].upper().replace("-", "_")
            # Create Poetry environment variable
            os.environ[f"POETRY_HTTP_BASIC_{source_name}_USERNAME"] = username
            os.environ[f"POETRY_HTTP_BASIC_{source_name}_PASSWORD"] = token

        # Add custom certificates
        if certificate:
            command_line = [poetry_executable, "config", f"certificates.{source['name']}.cert", certificate, "--local"]
            subprocess.run(command_line, check=True)


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
        "-m",
        "--disable-modern-installation",
        help="Disable Poetry modern installer.",
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
    optional_inputs.add_argument(
        "-lw",
        "--local_wheels",
        type=str,
        help="Directory to find the location of the whl files for SAF dependencies",
        default="",
        required=False,
    )
    optional_inputs.add_argument(
        "-z",
        "--env",
        type=str,
        help="Path to the environment file to be used to set environment variables.",
        default=".env",
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
        if os.path.isdir(DEPENDENCY_MANAGER_PATHS["common"]["build_system_venv"]):
            print("Delete existing poetry virtual environment")
            shutil.rmtree(DEPENDENCY_MANAGER_PATHS["common"]["build_system_venv"])
        # Remove poetry cache
        if os.path.isdir(DEPENDENCY_MANAGER_PATHS["common"]["cache_folder"]):
            print("Delete existing poetry cache")
            shutil.rmtree(DEPENDENCY_MANAGER_PATHS["common"]["cache_folder"])
        if args.force_clear_all:
            # Remove lock file
            if DEPENDENCY_MANAGER_PATHS["common"]["lock_file"]:
                if os.path.isfile(DEPENDENCY_MANAGER_PATHS["common"]["lock_file"]):
                    print("Delete existing poetry lock file")
                    os.remove(DEPENDENCY_MANAGER_PATHS["common"]["lock_file"])
    else:
        print("Skipped")
    print()


def update_lock_file_to_consider_local_wheels(args: object) -> None:
    """Specify in the poetry.lock file that some packages come from a local wheel file."""
    if not args.local_wheels:
        return

    print("Adapting lock file to consider local wheels.")
    subprocess.run(
        [
            DEPENDENCY_MANAGER_PATHS[sys.platform]["build_sys_exec"],
            "lock",
            "--no-update",
        ],
        check=True,
        shell=DEPENDENCY_MANAGER_PATHS[sys.platform]["shell"],
    )


def install_production_dependencies(args: object) -> None:
    """Install the package (mandatory requirements only)."""
    print("Install production dependencies")
    if "run" in args.dependencies:
        subprocess.run(
            [
                DEPENDENCY_MANAGER_PATHS[sys.platform]["build_sys_exec"],
                "install",
                "-vv",
            ],
            check=True,
            shell=DEPENDENCY_MANAGER_PATHS[sys.platform]["shell"],
        )
        print()
        return
    print("Skipped")
    print()


def install_optional_dependencies(args: object) -> None:
    """Install optional requirements (doc, tests, build or style)."""
    # Load configuration file
    configuration = toml.load(DEPENDENCY_MANAGER_PATHS["common"]["configuration_file"])
    # Install standard optional dependency groups
    for dependency_group in STANDARD_OPTIONAL_DEPENDENCY_GROUPS:
        print(f"Install {dependency_group} dependencies")
        if dependency_group in args.dependencies:
            # Install dependency group in the configuration file of the build system
            has_dependency_group = check_dependency_group(dependency_group, configuration)
            if has_dependency_group:
                print("Installing from build system configuration file.")
                subprocess.run(
                    [
                        DEPENDENCY_MANAGER_PATHS[sys.platform]["build_sys_exec"],
                        "install",
                        "--only",
                        dependency_group,
                        "-vv",
                    ],
                    check=True,
                    shell=DEPENDENCY_MANAGER_PATHS[sys.platform]["shell"],
                )
                print()
                continue
            # Alternatively search dependency group in the requirements folder
            requirements_file = os.path.join("requirements", f"requirements_{dependency_group}.txt")
            if os.path.exists(requirements_file):
                print("Installing from requirements file.")
                subprocess.run(
                    [
                        DEPENDENCY_MANAGER_PATHS[sys.platform]["poetry_python_executable"],
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
                    shell=DEPENDENCY_MANAGER_PATHS[sys.platform]["shell"],
                )
                print()
                continue
        print("Skipped")
        print()
    # Install extra optional dependency groups
    if args.extra_dependencies:
        for dependency_group in args.extra_dependencies:
            print(f"Install {dependency_group} dependencies")
            has_dependency_group = check_dependency_group(dependency_group, configuration)
            if has_dependency_group:
                subprocess.run(
                    [
                        DEPENDENCY_MANAGER_PATHS[sys.platform]["build_sys_exec"],
                        "install",
                        "--only",
                        dependency_group,
                        "-vv",
                    ],
                    check=True,
                    shell=DEPENDENCY_MANAGER_PATHS[sys.platform]["shell"],
                )
            else:
                print(f"No dependency group named {dependency_group}.")
                print("Skipped")
            print()


def install_dotnet_linux_dependencies():
    """Install .NET for Linux."""
    print("Install dotnet dependencies")
    if sys.platform == "linux":
        subprocess.run(
            """
            set -xe \
            && wget https://dot.net/v1/dotnet-install.sh \
            && chmod +x dotnet-install.sh \
            && ./dotnet-install.sh --install-dir /home/$USER/.dotnet --version 8.0.8 --runtime aspnetcore \
            && grep -qxF "DOTNET_ROOT=/home/$USER/.dotnet" /home/$USER/.bash_profile \
            || echo DOTNET_ROOT=/home/$USER/.dotnet >> /home/$USER/.bash_profile \
            && grep -qxF "PATH=\$PATH:/home/$USER/.dotnet" /home/$USER/.bash_profile \
            || echo "PATH=\$PATH:/home/$USER/.dotnet" >> /home/$USER/.bash_profile \
            && echo "\nsource /home/$USER/.bash_profile" >> ./.venv/bin/activate \
            && rm dotnet-install.sh
            """,
            check=True,
            shell=True,
        )


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

    if is_virtual_environment():
        raise Exception("Deactivate the current virtual environment before running this script.")

    load_env_file(args.env)

    # Check inputs consistency
    check_inputs(args)

    modify_toml_file_in_case_of_wheel_files(args)

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

    # Setup dependency management system ------------------------------------------------------------------------------

    print_section_header("Setup dependency management system", max_length=100)

    install_build_system(args)

    configure_build_system(args)

    # Install dependencies --------------------------------------------------------------------------------------------

    print_section_header("Install dependencies", max_length=100)

    update_lock_file_to_consider_local_wheels(args)

    install_production_dependencies(args)

    install_optional_dependencies(args)

    install_dotnet_linux_dependencies()

    # Back to current working directory
    os.chdir(working_directory)

    # Compute execution time
    elapsed_time = (time.time() - time_on) / 60  # in minutes

    print("You are all set!")
    print("Navigate to project root and activate your environment with one these commands:")
    print(rf"   - For Windows CMD       : {args.venv_name}\Scripts\activate.bat")
    print(rf"   - For Windows Powershell: {args.venv_name}\Scripts\Activate.ps1")
    print(rf"   - For Ubuntu            : source {args.venv_name}/bin/activate")
    print("Enjoy!")
    print()
    print("Execution time: %.1f minutes." % (elapsed_time))
    print()


# =================================================== [Execution] =================================================== #

if __name__ == "__main__":
    main()
