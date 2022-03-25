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
 
The ``ansys-templates`` tool is built on top of Python. To ensure a clean
installation you can use `pipx`_. This tool ensures an isolated installation of
any Python tool you want to use. You can install it by running:

.. code:: bash

   python -m pip install --user pipx

Ensure that `pipx`_ is in your ``PATH`` by running:

.. code:: bash

   python -m pipx ensurepath

If you encounter any issues when installing `pipx`_, refer to `pipx installation
guidelines`_.


Installing ansys-templates
--------------------------

Once you have installed `pipx`_, proceed with the installation of
``ansys-templates`` by running:

.. code:: bash

   python -m pipx install pyansys-templates


Upgrading ansys-templates
-------------------------

If you already have ``ansys-templates`` installed with `pipx`_, you can upgrade
to the latest version by running:

.. code:: bash

   python -m pipx upgrade pyansys-templates


Verify Your Installation
------------------------

Once installed, you can verify your installation by running:

.. code:: bash

   ansys-templates --help

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
.. _pipx installation guidelines: https://pypa.github.io/pipx/installation/
