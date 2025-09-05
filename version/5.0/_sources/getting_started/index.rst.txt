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


Installing ansys-templates
--------------------------

Once `pipx`_ is installed, proceed with the installation of
``ansys-templates`` with:

.. code:: bash

   python -m pipx install ansys-templates


Upgrading ansys-templates
-------------------------

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

   Ansys tool for creating new Ansys projects.

   Options:
     --help  Show this message and exit.

   Commands:
     list     List all available templates names.
     new      Create a new project from desired template.
     version  Display current version.

.. LINKS & REFERENCES
.. _pip: https://pypi.org/project/pip/
.. _pipx: https://github.com/pypa/pipx
.. _pipx installation guidelines: https://pipx.pypa.io/stable/installation/
