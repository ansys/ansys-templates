.. _ref_user_guide:


How to Use ansys-templates
==========================

Because ``ansys-templates`` is a command line tool, its usage is intended via
the command line. You can check available commands by running:

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


Listing Available Templates
---------------------------

You can list all available templates by running:

.. code:: bash

   ansys-templates list

Which outputs:


.. code:: text

   Available templates in ansys-templates are:

   pybasic: Create a baic Python Package.
   pyansys: Create a PyAnsys Python Package project.
   pyansys_advanced: Create an advanced PyAnsys Python Package project.



Creating a New Project
----------------------

You can create a new project using a given template by running ``ansys-templates
new`` and passing the name of the template you wish to use.

.. code:: bash

   ansys-templates new template_name

For example, to create a new Python Package project, use:

.. code:: bash

   ansys-templates new pybasic

Check available templates names using ``ansys-templates list`` command or just
run:

.. code:: bash

   ansys-templates new --help

For further information about how to use this command.


Checking Current Version
------------------------

For checking the your current installed version of ``ansys-templates`` simply run:

.. code:: bash

   ansys-templates version
