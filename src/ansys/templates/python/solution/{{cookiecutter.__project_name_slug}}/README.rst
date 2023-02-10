##############################################
Ansys Solutions {{cookiecutter.solution_name}}
##############################################

.. note::
  This content needs to be configured according to the project specifics. 


Introduction
============

.. note::
  Add here a description of the project.

Ansys Solutions {{cookiecutter.solution_name}}

  * Project name: **{{ cookiecutter.__project_name_slug }}**
  * Solution name: **{{ cookiecutter.__solution_name_slug }}**
  * Package name: **{{ cookiecutter.__pkg_name }}**


Installation
============

Prerequisites
-------------

Python version support
~~~~~~~~~~~~~~~~~~~~~~

.. note::
  Add here the supported Python versions.

For example:

  Officially Python 3.7 to 3.8.

Private PyPI servers
~~~~~~~~~~~~~~~~~~~~

Connection to Ansys-Solutions private PyPI server is required. Access is controlled via a ``Personal Access Token (PAT)`` which is available
in the `Solutions Developer's Guide <https://dev-docs.solutions.ansys.com/index.html>`_. To declare the PAT on your system:

  1. Visit the `Connecting to the private PyPI <https://dev-docs.solutions.ansys.com/how_to/get_started_org.html#connecting-to-the-private-pypi>`_ section of the `Solutions Developer's Guide <https://dev-docs.solutions.ansys.com/index.html>`_,
     navigate to the Private PyPI servers section and copy the token related to Ansys-Solutions PyPI.

  2. Create a system environment variable named SOLUTIONS_PRIVATE_PYPI_PAT and assign the token.
  
.. note::
  In addition to the Ansys-Solutions private PyPI server, you can add several private sources such as PyAnsys private PyPI server. 

Flagship products
~~~~~~~~~~~~~~~~~

.. note::
  Add here the name and the versions of Ansys flagship products needed to run the solution. 
  Remove this section if useless. 

For example:

  .. list-table:: Required flagship products
    :widths: 200 100
    :header-rows: 1

    * - Product
      - Versions

    * - SpaceClaim
      - R22.2 to latest

    * - Fluent
      - R23.1 to latest

    * - XXX
      - RXX.X

Setup the development environment
---------------------------------

In order to start using the solution or to develop inside the solution you need to install the Python ecosystem required.

``poetry`` is the dependency manager tool used in this project. The dependencies are declared in ``pyproject.toml`` at project root.

Automatic installation
~~~~~~~~~~~~~~~~~~~~~~

The automatic installation consists in running the setup_environment.py script at project root. Basically, this script creates a virtual environment,
and installs the dependency management tool ``poetry``. The ``-d`` option is used to specify the group of dependencies to install. For production
dependencies use ``-d run``, for doc dependencies use ``-d doc``, for tests dependencies ``-d tests``, and for build dependencies use ``-d build``.

To install the complete development environment follow these instructions:

1. Navigate to project root:

  .. code:: bash

    cd {{ cookiecutter.__project_name_slug }}

2. Setup the Python environment (the ``-d all`` option means that ``run``, ``doc``, ``tests``, and ``build`` dependencies will be installed):

  .. code:: bash

    python setup_environment.py -d all

3. Activate the virtual environment:

  * For Linux system:

    .. code:: bash

      source .venv/bin/activate

  * For Windows CMD:

    .. code:: bash

      .venv\Scripts\activate.bat

  * For Windows Powershell:

    .. code:: bash

      .venv\Scripts\Activate.ps1

From now on, all the commands listed in the documentation must be executed within the virtual environment.

Update dependencies
~~~~~~~~~~~~~~~~~~~

To add a new dependency or to update the version of an existing dependency use the ``poetry add`` command. 

For packages collected from public PyPI run:

  .. code:: bash

    poetry add <name-of-package>

For packages collected from Solutions private PyPI run:

  .. code:: bash

    poetry add <name-of-package> --source solutions-private-pypi

For packages collected from PyAnsys private PyPI run:

  .. code:: bash

    poetry add <name-of-package> --source pyansys-private-pypi

To request a specific version of a package add ``==<version>``:

  .. code:: bash

    poetry add <name-of-package>==<version>

Start the application
=====================

To start the application run the following command anywhere in the project:

  .. code:: bash

    saf run


Code style check
================

In this project, the following code style checks are required:

  * black 

  * isort

  * flake8

  * codespell

  * pydocstyle

All-in-one checks using pre-commit
----------------------------------

All those checks can be triggered with one single tool: ``pre-commit``. ``pre-commit`` is a GIT hook allowing to trigger all the code style commands at once at the point when you perform a git commit.
``pre-commit`` prevents you from forgetting to run the required actions against your code and it ensures the exact same style policies are applied. The code style policy is defined in the 
``.pre-commit-config.yaml`` at project root. 

Developers are not forced but encouraged to install ``pre-commit`` via:

  .. code:: bash

    python -m pip install pre-commit
        
  .. code:: bash
        
    pre-commit install

To run pre-commit:

  .. code:: bash

    pre-commit run --all-files --show-diff-on-failure

How to remove ``pre-commit``? 

  * Navigate to the git directory at the root of the repository

  * Select the hooks directory

  * Remove pre-commit file

Sequential checks
-----------------

Install code style requirements:

  .. code:: bash

    python -m pip install -r requirements/requirements_style.txt

Run black:

  .. code:: bash

    python -m black .

Run isort:

  .. code:: bash

    python -m isort .

Run flake8:

  .. code:: bash

    python -m flake8 .

Run codespell:

  .. code:: bash

    python -m codespell .


Testing
=======

**Unit tests** and **Integration tests** are executed via the ``pytest`` framework. 

To run the unit tests:

  .. code:: bash

    pytest tests/unit

To run the integration tests:

  .. code:: bash

    pytest tests/integration

To run all the tests:

  .. code:: bash

    pytest

To compute the coverage ratio and to generate a report:

  .. code:: bash

    pytest -p no:faulthandler --cov=ansys.solutions --cov-report=term --cov-report=xml --cov-report=html -vvv

To run the tests against multiple Python versions automatically:

  .. code:: bash

    tox -e py


Documentation
=============

Run the following command:

  .. code:: bash

    sphinx-build doc/source doc/build/html --color -vW -bhtml

Build
=====

Using the build module
----------------------

Build the package:

  .. code:: bash

    python -m build

Using poetry 
------------

Build the package:

  .. code:: bash

    poetry build

Automation using TOX
====================

``tox`` is a tool for automating all the commands listed above from code styling to testing and build. ``tox`` creates its own virtual environment so anything
being tested is isolated from the project in order to guarantee project's integrity. The following environments commands are provided:

  * **tox -e style**: will check for coding style quality.

  * **tox -e py**: checks for unit tests.

  * **tox -e py-coverage**: checks for unit testing and code coverage.

  * **tox -e doc**: checks for documentation building process.

  * **tox -e build**: checks source code build.
