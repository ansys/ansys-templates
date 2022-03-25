.. _ref_user_guide:


How to Use PyAnsys Templates
============================

Because ``pyansys-templates`` is a command line tool, its usage is intended via
the command line. You can check available commands with:

.. code:: bash

   pyansys-templates --help

The following help content is returned:

.. code:: text

   Usage: pyansys-templates [OPTIONS] COMMAND [ARGS]...

   Ansys tool for creating Python projects.
   
   Options:
     --help  Show this message and exit.
   
   Commands:
     list  List all available templates names.
     new   Create a new project from desired template.
     version  Display current version.


Listing All Templates
---------------------

You can list all templates with:

.. code:: bash

   ansys-templates list

The following templates are returned:

.. code:: text

   Available templates in pyansys-templates are:

   pybasic: Create a basic Python Package.
   pyansys: Create a PyAnsys Python Package project.
   pyansys_advanced: Create an advanced PyAnsys Python Package project.


Creating a New PyAnsys Project
------------------------------

You can use a given template to create a new PyAnsys project with ``ansys-templates
new`` followed by the name of the template that you want to use:

.. code:: bash

   pyansys-templates new <template_name>

For example, to create a new Python Package project with the pybasic template:

.. code:: bash

   pyansys-templates new pybasic

You can see all templates available with ``pyansys-templates list``. Or, see more
information about how to use this command with:

.. code:: bash

   pyansys-templates new --help

Checking the Current Version
----------------------------

Check the your current installed version of PyAnsys templates with:

.. code:: bash

   pyansys-templates version
