.. _ref_user_guide:


How to use ``ansys-templates``
==============================

Because ``ansys-templates`` is a command line tool, its usage is intended via
the command line. You can check available commands with:

.. code:: bash

   ansys-templates --help

The following help content is returned:

.. code:: text

   Usage: ansys-templates [OPTIONS] COMMAND [ARGS]...

   Ansys tool for creating Python projects.
   
   Options:
     --help  Show this message and exit.
   
   Commands:
     list  List all available templates names.
     new   Create a new project from desired template.
     version  Display current version.


Listing all templates
---------------------

You can list all templates with:

.. code:: bash

   ansys-templates list

The following templates are returned:

.. code:: text

   Available templates in ``ansys-templates`` are:

   pybasic: Create a basic Python Package.
   pyansys: Create a PyAnsys Python Package project.
   pyansys-advanced: Create an advanced PyAnsys Python Package project.
   pyace: Create a Python project for any method developers.
   pyace-flask: Create a Flask project initialized for any developer.
   pyace-grpc: Create gRPC project initialized for any developer.
   pyace-fast: Create a FastAPI project initialized for any developer.


Creating a new PyAnsys project
------------------------------

You can use a given template to create a new PyAnsys project with ``ansys-templates
new`` followed by the name of the template that you want to use:

.. code:: bash

   ansys-templates new <template_name>

For example, to create a new Python Package project with the pybasic template:

.. code:: bash

   ansys-templates new pybasic

You can see all templates available with ``ansys-templates list``. Or, see more
information about how to use this command with:

.. code:: bash

   ansys-templates new --help

Checking the current version
----------------------------

Check the your current installed version of PyAnsys templates with:

.. code:: bash

   ansys-templates version
