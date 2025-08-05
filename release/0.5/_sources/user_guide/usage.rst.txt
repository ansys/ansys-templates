.. Copyright (C) 2023 ANSYS, Inc. and/or its affiliates.
.. SPDX-License-Identifier: MIT
..
..
.. Permission is hereby granted, free of charge, to any person obtaining a copy
.. of this software and associated documentation files (the "Software"), to deal
.. in the Software without restriction, including without limitation the rights
.. to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
.. copies of the Software, and to permit persons to whom the Software is
.. furnished to do so, subject to the following conditions:
..
.. The above copyright notice and this permission notice shall be included in all
.. copies or substantial portions of the Software.
..
.. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
.. IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
.. FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
.. AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
.. LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
.. OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
.. SOFTWARE.

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
