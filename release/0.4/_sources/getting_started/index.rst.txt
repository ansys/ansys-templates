.. _ref_getting_started:

Getting started
===============

To successfully install ``ansys-templates``, carefully read all instructions on this page.


Before installing
-----------------

Several requirements must be met before you install
``ansys-templates``.


Upgrading ``pip``
^^^^^^^^^^^^^^^^^

Upgrade `pip`_ with:

.. code:: bash

   python -m pip install --upgrade pip


Installing ``pipx``
^^^^^^^^^^^^^^^^^^^
 
The ``ansys-templates`` tool is built on top of Python. To ensure a clean
installation, you can use `pipx`_. It ensures an isolated installation of
any Python tool that you want to use. 

Install `pipx`_ with:

.. code:: bash

   python -m pip install --user pipx

Ensure that `pipx`_ is in your ``PATH`` with:

.. code:: bash

   python -m pipx ensurepath

If you encounter any issues when installing `pipx`_, see `pipx installation
guidelines`_.


Installing ``ansys-templates``
------------------------------

Once `pipx`_ is installed, proceed with the installation of
``ansys-templates`` with:

.. code:: bash

   python -m pipx install ansys-templates


Upgrading ``ansys-templates``
-----------------------------

If you already have ``ansys-templates`` installed with `pipx`_, you can upgrade
to the latest version with:

.. code:: bash

   python -m pipx upgrade ansys-templates


Verify your installation
------------------------

Once installed, you can verify your installation with:

.. code:: bash

   ansys-templates --help

The following code is returned:

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
