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


Installation
============

Prerequisites
-------------

.. list-table::
  :widths: 15 40

  * - **Operating system**
    - Windows 10
  * - **Python distribution**
    - From **3.8** to **3.10**.
  * - **IDE**
    - `Visual Studio Code <https://code.visualstudio.com/download#>`_
  * - **Web framework**
    - `Dash <https://dash.plotly.com/>`_
  * - **Software**
    - *List here the required software, if any.*
  * - **Tokens**
    - *Visit the `Solutions Developer's Guide <https://dev-docs.solutions.ansys.com/solution_journey/journey_prepare/connect_to_private_pypi>`_ to learn how to set the required tokens.*
  * - **Environment variables**
    - *List here the required environment variables, if any.*

Setting up the development environment
---------------------------------------

1. Clone the repository:

   .. code:: bash

     git clone https://github.com/Solution-Applications/{{ cookiecutter.__project_name_slug }}

2. Navigate to the cloned project directory:

   .. code:: bash

    cd {{ cookiecutter.__project_name_slug }}

3. Install ``toml`` and ``packaging`` on your system environment:

   .. code:: bash

     pip install toml packaging

4. Install the production dependencies:

  .. code:: bash

    python setup_environment.py -d run

5. Activate the virtual environment:

  * For Windows CMD:

    .. code:: bash

      .venv\Scripts\activate.bat

  * For Windows Powershell:

    .. code:: bash

      .venv\Scripts\Activate.ps1

From now on, all the commands must be executed within the virtual environment.


Starting the solution
=====================

To start the solution run the following command anywhere in the project:

  .. code:: bash

    saf run


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
