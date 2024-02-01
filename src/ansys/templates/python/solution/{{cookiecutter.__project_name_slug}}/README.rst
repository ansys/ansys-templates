##############################################
{{cookiecutter.solution_name}}
##############################################
|python|


Installation
============

Prerequisites
-------------

.. list-table::
  :widths: 15 40

  * - **Operating system**
    - Windows 10
  * - **Python distribution**
    - Python distribution between **3.8** to **3.10**.
  * - **IDE**
    - `Visual Studio Code <https://code.visualstudio.com/download#>`_.
  * - **Web framework**
    - `Dash <https://dash.plotly.com/>`_
  * - **Software**
    - | <replace-with-product-name>
      | <add-another-product-name>
      | <repeat-for-each-product>
  * - **Tokens**
    - The environment variables ``PYANSYS_PRIVATE_PYPI_PAT`` is set with the corresponding token which can be find `here <https://dev-docs.solutions.ansys.com/solution_journey/journey_prepare/connect_to_private_pypi.html>`_.


Setting up the development environment
---------------------------------------

1. Clone the repository:

   .. code:: bash

     git clone https://github.com/ansys-internal/{{ cookiecutter.__project_name_slug }}

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


Start the solution
==================

To start the solution run the following command anywhere in the project:

  .. code:: bash

    saf run


Documentation
=============

Refer to the `Solution Developer's Guide <https://dev-docs.solutions.ansys.com/index.html>`_ to get more information on how to
get started with building solutions.

Refer to the documentations below to get more details on how to use the Solution Application Framework (SAF):

* `GLOW doc <https://saf.docs.solutions.ansys.com/version/stable/>`_
* `Portal doc <https://potential-adventure-ovlqkq9.pages.github.io/version/dev/>`_


License
=======

Copyright (c) ANSYS Inc. All rights reserved.


.. BADGES

.. |python| image:: https://img.shields.io/badge/Python-3.8–3.10-blue.svg
