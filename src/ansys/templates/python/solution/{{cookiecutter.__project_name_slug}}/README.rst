##############################################
{{cookiecutter.solution_name}}
##############################################
|python|

.. note::
  This content needs to be configured according to the project specifics.


Introduction
============

.. note::
  Add here a description of the project.


Prerequisites
=============

Operation system
----------------

Windows 10 to latest.

Python
------

Officially Python 3.8 to 3.10. Before starting the installation run ``python --version`` and check that it fits with the supported versions.

Token
-----

Connection to the **Solutions** private PyPI server is required. The access is controlled via a token. Create a system environment variable named ``SOLUTIONS_PRIVATE_PYPI_PAT``
and assign it with the **Solutions** token provided in `Connecting to the private PyPI <https://dev-docs.solutions.ansys.com/solution_journey/journey_prepare/connect_to_private_pypi.html>`_.

Software
--------

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


Installation
============

1. Clone the repository:

   .. code:: bash

     git clone https://github.com/Solution-Applications/{{ cookiecutter.__project_name_slug }}

2. Navigate to the cloned project directory:

   .. code:: bash

    cd {{ cookiecutter.__project_name_slug }}


Start the solution with a local installation
============================================

To start the solution using a desktop orchestrator run the following commands in the root of the project:


1. Install ``toml`` and ``packaging`` on your system environment:

   .. code:: bash

     pip install toml packaging

2. Install the production and desktop dependencies:

  .. code:: bash

    python setup_environment.py -d run desktop

3. Activate the virtual environment:

  * For Windows CMD:

    .. code:: bash

      .venv\Scripts\activate.bat

  * For Windows Powershell:

    .. code:: bash

      .venv\Scripts\Activate.ps1

4. Launch the solution:

  .. code:: bash

    saf run


Start the solution using Docker
===============================

To start the solution using a docker run the following commands in the root of the project:


1. Build docker images:

  .. code:: bash

    docker build -t my_solution_api:latest --target my_solution_api --build-arg SOLUTIONS_PRIVATE_PYPI_PAT=$SOLUTIONS_PRIVATE_PYPI_PAT .
{% if cookiecutter.with_dash_ui == "yes" %}
    docker build -t my_solution_ui:latest --target my_solution_ui --build-arg SOLUTIONS_PRIVATE_PYPI_PAT=$SOLUTIONS_PRIVATE_PYPI_PAT .
{% endif %}
2. Launch the solution:

  .. code:: bash

    docker compose up


Documentation
=============

Refer to the `Solution Developer's Guide <https://dev-docs.solutions.ansys.com/index.html>`_ to get more information on how to the
get started with solutions.

To develop your solution, refer to the Solution Application Framework (SAF) documentations:

* `GLOW doc <https://saf.docs.solutions.ansys.com/version/stable/>`_
* `Portal doc <https://potential-adventure-ovlqkq9.pages.github.io/version/dev/>`_


License
=======

Copyright (c) ANSYS Inc. All rights reserved.


.. BADGES

.. |python| image:: https://img.shields.io/badge/Python-3.8–3.10-blue.svg
