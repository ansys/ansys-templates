.. _ref_getting_started:

Getting Started
===============

Please, carefully read all the instructions in this page in order to achieve a
successfully install of ``ansys-templates``.


Before Installing
-----------------

Several requirements need to be fulfilled before you can proceed installing
``ansys-templates`` tool.


Upgrading pip
^^^^^^^^^^^^^

Before installing the ``ansys-templates``, it is advisable to upgrade `pip`_ by
running:

.. code:: bash

   python -m pip install --upgrade pip


Installing pipx
^^^^^^^^^^^^^^^
 
The ``ansys-templates`` tool is build on top of Python. To ensure a clean
installation you can use `pipx`_. This tool ensures an isolated installation of
any Python tool you want to use. You can install it by running:

.. code:: bash

   python -m pip install --user pipx

Ensure that `pipx`_ is in your ``PATH`` by running:

.. code:: bash

   pipx ensurepath

If you encounter any issues when installing `pip`_, refer to `pipx installation
guidelines`_.


Installing ansys-templates
--------------------------

Since ``ansys-templates`` makes use of Python, it is advisable to install it
using `pipx`_ by following `pipx installation guidelines`_. Finally, you can
install ``ansys-templates`` by running:

.. code:: bash

   pipx install git+https://github.com/pyansys/pyansys-template



Verify Your Installation
------------------------

Once installed, you can verify your installation by running:

.. code:: bash

   pipx run ansys-templates --help

Which returns:

.. code:: text

   Usage: ansys-templates [OPTIONS] COMMAND [ARGS]...

   Ansys tool for creating Python projects.
   
   Options:
     --help  Show this message and exit.
   
   Commands:
     list  List all available templates names.
     new   Create a new project from desired template.
     version  Display current version.

.. LINKS & REFERENCES
.. _pip: https://pypi.org/project/pip/
.. _pipx: https://github.com/pypa/pipx
.. _pipx installation guidelines: https://github.com/pypa/pipx#install-pipx
