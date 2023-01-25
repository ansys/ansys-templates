# ©2022, ANSYS Inc. Unauthorized use, distribution or duplication is prohibited.

"""
A Python script to automate the setup of the Python ecosystem of a solution or framework.
"""

# ==================================================== [Imports] ==================================================== #

import argparse
import os
from packaging import version
from pathlib import Path, PurePath
import platform
import re
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


def read_integers_from_string(string):
    """
    Scan a string and extract integers.

    The regex matches any digit character (0-9).
    """
    return re.findall("\d+", string)


def get_lower_version_from_python_specification(lower_specification):
    """Take a lower specification and convert it to the lowest authorized python version."""
    lower_version = ".".join(read_integers_from_string(lower_specification))
    if lower_specification.startswith(">") and "=" not in lower_specification:
        lower_version_splitted = lower_version.split(".")
        lower_version_splitted[-1] = str(int(lower_version_splitted[-1]) + 1)
        lower_version = ".".join(lower_version_splitted)
    return lower_version


def get_upper_version_from_python_specification(upper_specification):
    """Take a upper specification and convert it to the highest authorized python version."""
    upper_version = ".".join(read_integers_from_string(upper_specification))
    if upper_specification.startswith("<") and "=" not in upper_specification:
        upper_version_splitted = upper_version.split(".")
        upper_version_splitted[-1] = str(int(upper_version_splitted[-1]) - 1)
        upper_version = ".".join(upper_version_splitted)
    return upper_version


def get_compatible_python_versions(configuration_file):
    """Reads a pyproject.toml file and axtract the list of compatible python versions."""
    configuration = toml.load(configuration_file)
    python_compatibility = configuration["tool"]["poetry"]["dependencies"]["python"].replace(" ", "")
    if "," in python_compatibility:
        # Process lower version
        lower_specification = python_compatibility.split(",")[0]
        lower_version = get_lower_version_from_python_specification(lower_specification)
        # Process upper version
        upper_specification = python_compatibility.split(",")[1]
        upper_version = get_upper_version_from_python_specification(upper_specification)
    else:
        if python_compatibility.startswith(">"):
            lower_version = get_lower_version_from_python_specification(python_compatibility)
            upper_version = "3.10"
        elif python_compatibility.startswith("<"):
            lower_version = "3.7"
            upper_version = get_lower_version_from_python_specification(python_compatibility)
        else:
            raise Exception("Unable to interpret python version specification.")
    if len(lower_version.split(".")) == 2:
        lower_version += ".0"
    if len(upper_version.split(".")) == 2:
        upper_version += ".0"
    return lower_version, upper_version


def get_python_version():
    """Get Python version."""
    return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"


def check_python_version(configuration_file):
    """Check if the current python version is compatible with the pyproject.toml specifications."""
    setup_version = get_python_version()
    lower_version, upper_version = get_compatible_python_versions(configuration_file)

    if version.parse(setup_version) < version.parse(lower_version) or version.parse(setup_version) > version.parse(upper_version):
        raise Exception(f"Python version is wrong. Project required a version in the range {lower_version}, {upper_version}. Current version is {setup_version}.")


def get_python_package(
    package_name: str,
    package_version: str = "*",
    method: str = "install",
    pypi_url: str = "https://pypi.org/simple",
    private_pypi_token_name: str = None,
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
            raise Exception(
                "Environment variable {private_pypi_token_name} does not exist."
            )
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
    returncode, stdout, stderr = run_command(command, display_output=False)
    if returncode != 0:
        print(stdout)
        raise Exception("Command failed with error.")


def remove_scheme_from_url(url):
    """Remove the scheme part of a URL."""
    items = url.split("://")
    if len(items) == 2:
        return items[0], items[1]
    else:
        raise Exception(f"Fail to return the URL without the scheme part for {url}.")


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
    subprocess.run(
        [python_executable, "-m", "pip", "install", "--upgrade", "pip"],
        check=True,
        shell=True,
    )


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
        "-f",
        "--force-clear",
        help="Clean-up the workspace. Delete existing .venv and poteyr.lock.",
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
            print(
                f"Warning: Poetry expects the name of the virtual environment name to be .venv. {old_name} is renamed {args.venv_name}."
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
    # Check python version
    check_python_version("pyproject.toml")


def show_parameters(args):
    """Display the parameters to the console before proceeding to work."""
    print("OS                       : %s" % (platform.system()))
    print("Python version           : %s" % (get_python_version()))
    print("Virtual environment name : %s" % (args.venv_name))
    print("Run dependencies         : %s" % ("yes" if "run" in args.dependencies else "no"))
    print("Doc dependencies         : %s" % ("yes" if "doc" in args.dependencies else "no"))
    print("Tests dependencies       : %s" % ("yes" if "tests" in args.dependencies else "no"))
    print("Build dependencies       : %s" % ("yes" if "build" in args.dependencies else "no"))
    print("Style dependencies       : %s" % ("yes" if "style" in args.dependencies else "no"))
    print("Build system             : %s" % (args.build_system))
    print("Build system version     : %s" % (args.build_system_version))
    print("Build distribution       : %s" % ("yes" if args.build else "no"))
    print("Build method             : %s" % (args.build_method))
    print("Credentials management   : %s" % (args.credentials_management))
    print("")


def clear_workspace():
    """Remove residual items form previous installation (like venv directory, lock file ...)."""
    # Remove virtual environment
    if os.path.isdir(".venv"):
        print("Delete existing virtual environment")
        shutil.rmtree(".venv")
    # Remove lock file
    if os.path.isfile("poetry.lock"):
        sys.stdout.write("Delete existing poetry lock file\n")
        os.remove("poetry.lock")


def get_private_sources(configuration_file):
    """Get list of private sources from configuration file."""
    package_config = toml.load(configuration_file)
    try:
        private_sources = package_config["tool"]["poetry"]["source"]
    except:
        private_sources = []
    return private_sources


def get_package_data(configuration_file):
    """Get list of package data to include in the source distribution."""
    package_config = toml.load(configuration_file)
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
    print("Clean-up existing poetry configurations")
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
        print("Declare credentials for %s" % (source["name"]))
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


def install_production_dependencies(args):
    """Install the package (mandatory requirements only)."""
    subprocess.run([".venv/Scripts/poetry", "install", "-v"], check=True)


def install_optional_dependencies(dependency_group):
    """Install optional requirements (doc, tests, build or style)."""
    file = os.path.join("requirements", f"requirements_{dependency_group}.txt")
    command = f".venv/Scripts/python -m pip install -r {file} --no-warn-conflicts"
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
                print("Warning: package_data %s exists in %s. No override." % (data, destination))
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


def create_virtual_environùent(venv_name: str = None, python_executable: str = sys.executable) -> None:
    """Create a virtual environment."""
    print("Create virtual environment")
    subprocess.run([python_executable, "-m", "venv", venv_name], check=True, shell=True)
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
    # Read command line inputs
    args = parser()
    # Check inputs consistency
    check_inputs(args)

    # Display header
    print("==============================================================================================")
    print("Setup Environment")
    print("==============================================================================================")
    print("")

    print("")
    print("Setup session --------------------------------------------------------------------------------")
    print("")

    # Parameters
    show_parameters(args)

    print("")
    print("Clear workspace ------------------------------------------------------------------------------")
    print("")

    # Clean-up workspace
    if args.force_clear:
        clear_workspace()
    else:
        print("Skipped")

    print("")
    print("Setup virtual environment --------------------------------------------------------------------")
    print("")

    # Create virtual environment
    print("Create virtual environment")
    if os.path.isdir(args.venv_name) and not args.force_clear:
        print("Skipped")
    else:
        subprocess.run([sys.executable, "-m", "venv", ".venv"])
    print("")

    # Upgrade to latest pip version
    print("Upgrade to latest pip version")
    upgrade_pip(python_executable=r".\.venv\Scripts\python")
    print("")

    print("Setup build system ---------------------------------------------------------------------------")
    print("")

    # Install build system
    print("Install build system")
    get_python_package(
        args.build_system, args.build_system_version,  method="install", python_executable=r".\.venv\Scripts\python"
    )

    # Configure build system
    print("Configure build system")
    configure_build_system(args)
    print("")

    print("Install requirements -------------------------------------------------------------------------")
    print("")

    # Install package dependencies
    print("Install run dependencies")
    if "run" in args.dependencies:
        install_production_dependencies(args)
    else:
        print("Skipped")
    print("")

    # Install optional dependencies
    for dependency_group in ["doc", "tests", "build", "style"]:
        print("Install %s dependencies" % (dependency_group))
        if dependency_group in args.dependencies:
            install_optional_dependencies(dependency_group)
        else:
            print("Skipped")
        print("")

    print("Build distribution ---------------------------------------------------------------------------")
    print("")

    # Build distribution
    if args.build:
        # Include package data
        print("Include package data")
        include_package_data(args)
        print("")
        # Build distribution
        print("Build distribution")
        build_distribution(args)
        print("")
    else:
        print("Skipped")
    print("")

    # Back to current working directory
    os.chdir(working_directory)

    # Compute execution time
    elapsed_time = (time.time() - time_on) / 60  # in minutes

    print("")
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
