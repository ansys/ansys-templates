{{cookiecutter.__project_name_slug}}
====================================
|python|

.. note::
  This content needs to be configured according to the project specifics.

|                          |         |
| ------------------------ | ------- |
| Solution Owner           | XXXXXXX |
| Solution Product Manager | XXXXXXX |
| Domain ``SME``           | XXXXXXX |
| Development Manager      | XXXXXXX |
| Solution development     | XXXXXXX |
| UI/UX                    | XXXXXXX |
| DevOps                   | XXXXXXX |
| Documentation            | XXXXXXX |


# Prerequisites

| Prerequisite | Description |
|--------------|-------------|
| Operating system | Windows 10 or Ubuntu |
| Python distribution | Python 3.10 |
| IDE | [Visual Studio Code](https://code.visualstudio.com/download#) |
| Virtualization | [Docker](https://www.docker.com/) |
| Environment variables | - Set ``PYANSYS_PYPI_PRIVATE_PAT`` with the corresponding [token](https://dev-docs.solutions.ansys.com/version/dev/solution_journey/journey_prepare/connect_to_private_pypi.html).<br>- Set ``MACHINE_IP`` with the IP address of your machine (only for containerized mode) |
| Software | <replace-with-product-name><br><replace-with-product-name> |


# Local Desktop Installation

## Setup

1. Navigate to project root:

```bash
cd {{ cookiecutter.__project_name_slug }}
```

2. Install ``toml`` and ``packaging`` on your system environment:

```bash
pip install toml packaging
```

3. Install the production dependencies:

```bash
python setup_environment.py -d run ui desktop
```

4. Activate the virtual environment:

    - For Windows CMD:

    ```bash
    .venv\Scripts\activate.bat
    ```

    - For Windows Powershell:

    ```bash
    .venv\Scripts\activate.bat
    ```

    - For Ubuntu:

    ```bash
    source .venv/bin/activate
    ```

From now on, all the commands must be executed within the virtual environment.

## Start

To start the solution run the following command anywhere in the project:

```bash
saf run
```

## Generate an executable installer

To generate an executable installer from the solution application:

1. Install the build dependencies:

```bash
poetry install --only build
```

2. Run the ``saf package`` command:

```bash
saf package --solution-display-name <display-name>
```

# Containerized Desktop Installation

## Setup

To run the containerized solution, you need to set the ``MACHINE_IP`` environment variable with:

- The IP address of your machine if you use Docker Desktop

- The WSL IP address of your machine if you use WSL.

## Start

1. Navigate to project root:

```bash
cd {{ cookiecutter.__project_name_slug }}
```

2. Start the services:

```bash
docker compose -f deployments/dev/compose-dev.yaml up --build
```

Wait for all services to start.

1. Open a web page and reach the GLOW API Swager UI: ``http://localhost:8000/docs``

2. Create a project using the ``Create Project`` post request.

3. Copy the project name from the response. It should be like: ``projects/<project-id>``.

4. Open a web page and reach the Solution UI: ``http://localhost:8001/projects/<project-id>``.

Now you can walkthrough the solution workflow.

## Stop

To shutdown the application:

1. CTRL+C in the terminal where you executed the previous docker command.

2. Turn the docker containers down:

```bash
docker compose -f deployments/dev/compose-dev.yaml down
```

# Documentation

Refer to the `Solution Developer's Guide [Solution Developer's Guide](https://dev-docs.solutions.ansys.com/index.html) to get more information on how to get started with solutions.


# License

Copyright (c) ANSYS Inc. All rights reserved.
