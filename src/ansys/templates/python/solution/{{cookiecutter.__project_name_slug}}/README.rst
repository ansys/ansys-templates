#######################################
Ansys Solutions {{cookiecutter.solution_name}}
#######################################

Introduction
============

Ansys Solutions {{cookiecutter.solution_name}}

  * Solution name: **{{ cookiecutter.__solution_name_slug }}**
  * Package name: **{{ cookiecutter.__pkg_name }}**

Installation
============

Prerequisites
-------------

Python version support
~~~~~~~~~~~~~~~~~~~~~~

Officially Python 3.7 to 3.9.

Private PyPI server
~~~~~~~~~~~~~~~~~~~

Connection to Ansys-Solutions private PyPI server is required. Access is controlled via a ``Personal Access Token (PAT)`` which is available
in the `Solutions Developer's Guide <https://dev-docs.solutions.ansys.com/index.html>`_. To declare the PAT on your system:

  1. Visit the `Connecting to the private PyPI <https://dev-docs.solutions.ansys.com/how_to/get_started_org.html#connecting-to-the-private-pypi>`_ section of the `Solutions Developer's Guide <https://dev-docs.solutions.ansys.com/index.html>`_,
     navigate to the Private PyPI servers section and copy the token related to Ansys-Solutions PyPI.

  2. Create a system environment variable named SOLUTIONS_PRIVATE_PYPI_PAT and assign the token.
  
Setup the development environment
---------------------------------

This procedure is intended for software developers that will contribute to the package maintenance and development. 

Setup the default configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Setup the Python environment:

  .. code:: bash

    python setup_environment.py -d all

2. Activate the virtual environment:

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

You can add dependencies to the package by updating the [tool.poetry.dependencies] section in the pyproject.toml. file.
Each time the dependencies are changed it is important to update the virtual environment by running the following command:

  .. code:: bash

    poetry install

Start the application
=====================

To start the application:

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
