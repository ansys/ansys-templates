.. _docker-installation:

Docker Installation
###################

Prerequisites
=============

.. list-table:: Prerequisites
    :header-rows: 1

    * - Prerequisite
      - Description

    * - Operating system
      - Windows 10 or Ubuntu

    * - Python distribution
      - Python 3.10

    * - IDE
      - `Visual Studio Code <https://code.visualstudio.com/download#>`_

    * - Virtualization
      - `Docker <https://www.docker.com/>`_

    * - Environment variables
      - | ``PYANSYS_PYPI_PRIVATE_PAT`` set to the corresponding `token <https://dev-docs.solutions.ansys.com/solution_journey/journey_prepare/connect_to_private_pypi.html>`_
        | ``MACHINE_IP`` set to the machine IP address.

Setup & Start
=============

1. Navigate to project root:

.. code-block:: bash

  cd {{ cookiecutter.__project_name_slug }}

2. Start the services:

.. code-block:: bash

  docker compose -f deployments/dev/compose-dev.yaml up --build

.. important::

  Wait for all services to start.

1. Open a web page and reach the GLOW API Swager UI: ``http://localhost:8000/docs``

2. Create a project using the ``Create Project`` post request.

3. Copy the project name from the response. It should be like: ``projects/<project-id>``.

4. Open a web page and reach the Solution UI: ``http://localhost:8001/projects/<project-id>``.

Now you can walkthrough the solution workflow.

Stop
====

To shutdown the application:

1. CTRL+C in the terminal where you executed the previous docker command.

2. Turn the docker containers down:

.. code-block:: bash

  docker compose -f deployments/dev/compose-dev.yaml down
