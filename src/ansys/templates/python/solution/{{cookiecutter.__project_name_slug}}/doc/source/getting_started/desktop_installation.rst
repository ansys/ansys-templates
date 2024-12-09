.. _desktop-installation:

Desktop Installation
####################

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

    * - Environment variables
      - ``PYANSYS_PYPI_PRIVATE_PAT`` set to the corresponding `token <https://dev-docs.solutions.ansys.com/solution_journey/journey_prepare/connect_to_private_pypi.html>`_

Setup
=====

1. Navigate to project root:

.. code-block:: bash

    cd {{ cookiecutter.__project_name_slug }}

2. Install ``toml`` and ``packaging`` on your system environment:

.. code-block:: bash

    pip install toml packaging

3. Install the production dependencies:

.. code-block:: bash

    python setup_environment.py -d run ui desktop

4. Activate the virtual environment:

.. tab-set::

    .. tab-item:: Windows CMD

        .. code-block:: bash

            .venv\Scripts\activate.bat

    .. tab-item:: Windows Powershell

        .. code-block:: bash

            .venv\Scripts\Activate.ps1

    .. tab-item:: Linux/UNIX

        .. code-block:: bash

            source .venv/bin/activate

.. important::

    From now on, all the commands must be executed within the virtual environment.

Start
=====

To start the solution run the following command anywhere in the project:

.. code-block:: bash

    saf run

The Portal UI will start in a desktop window.

.. list-table:: Key options
    :header-rows: 1

    * - Option
      - Description
      - Usage

    * - ``debug``
      - Activate debug mode.
      - ``saf run --debug``

    * - ``project <project-name>``
      - Bypass SAF Portal UI and start a specific project.
      - ``saf run --project <project-name>``

Check the code style
====================

.. warning::

    Make sure the virtual environment is activated.

1. Install the tests dependencies:

.. code-block:: bash

    poetry install --only tests

2. Run the checks:

.. code-block:: bash

    tox -e style

Build the documentation
=======================

.. warning::

    Make sure the virtual environment is activated.

1. Install the documentation dependencies:

.. code-block:: bash

    poetry install --only doc

2. Build the documentation:

.. code-block:: bash

    sphinx-build doc/source doc/build/html --color -vW -bhtml

Run unit tests
==============

.. warning::

    Make sure the virtual environment is activated.

1. Install the tests dependencies:

.. code-block:: bash

    poetry install --only tests

2. Run the tests:

.. code-block:: bash

    pytest
