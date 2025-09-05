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

Templates
=========

All the available templates in ``ansys-templates`` can be found on this page.

For quick-reference, the following table provides an overview of the main
capabilities and features of each template:

+--------------------------------+-----------------------+-----------------+---------+----------+----------------+---------+
| Template                       | setup.py              | pyproject.toml  | Actions | tox.ini  | requirements/  | Docker  |
+================================+=======================+=================+=========+==========+================+=========+
| :ref:`doc-project`             |                       |                 |  ``X``  |  ``X``   |  ``X``         |         |
+--------------------------------+-----------------------+-----------------+---------+----------+----------------+---------+
| :ref:`pybasic`                 | ``X``                 |                 |         |          |                |         |
+--------------------------------+-----------------------+-----------------+---------+----------+----------------+---------+
| :ref:`pyansys`                 |  ``X``                |  ``X``          |  ``X``  |          |                |         |
+--------------------------------+-----------------------+-----------------+---------+----------+----------------+---------+
| :ref:`pyansys-advanced`        |  ``X``                |  ``X``          |  ``X``  |  ``X``   |  ``X``         |         |
+--------------------------------+-----------------------+-----------------+---------+----------+----------------+---------+
| :ref:`pyansys-openapi-client`  |                       |                 |         |          |                |         |
+--------------------------------+-----------------------+-----------------+---------+----------+----------------+---------+
| :ref:`pyace`                   |  ``X``                |  ``X``          |  ``X``  |  ``X``   |  ``X``         |  ``X``  |
+--------------------------------+-----------------------+-----------------+---------+----------+----------------+---------+
| :ref:`pyace-fast`              |  ``X``                |  ``X``          |  ``X``  |  ``X``   |  ``X``         |  ``X``  |
+--------------------------------+-----------------------+-----------------+---------+----------+----------------+---------+
| :ref:`pyace-flask`             |  ``X``                |  ``X``          |  ``X``  |  ``X``   |  ``X``         |  ``X``  |
+--------------------------------+-----------------------+-----------------+---------+----------+----------------+---------+
| :ref:`pyace-grpc`              |  ``X``                |  ``X``          |  ``X``  |  ``X``   |  ``X``         |  ``X``  |
+--------------------------------+-----------------------+-----------------+---------+----------+----------------+---------+
| :ref:`solution`                |                       |  ``X``          |  ``X``  |  ``X``   |  ``X``         |         |
+--------------------------------+-----------------------+-----------------+---------+----------+----------------+---------+

.. note::

   In the ``demo/`` branches of the repository you can find rendered versions
   for each one of the templates. Take a look to these branches for having a
   better idea on the final project layout.

doc-project
-----------
This template renders a documentation project based on Sphinx. You can chose
between Ansys or PyAnsys logos together with the color theme.

Main features of this package are:

- Ability to choose between Ansys or PyAnsys logos.
- Includes GitHub workflows (actions).
- All ``requirements_*.txt`` are contained in a ``requirements_/`` directory.
- Includes a ``tox.ini`` file.

To create a new project using this template by running:

.. code-block:: text

    ansys-templates new doc-project

.. admonition:: Link to demo

    `ansys-templates/demo - doc-project <https://github.com/ansys/ansys-templates/tree/demo/doc-project>`_

pybasic
-------
This template renders to a basic Python project. It does not follow the Ansys
namespace, meaning that a ``src/library/`` layout is produced instead of the
``src/ansys/product/library`` one.

Main features of this package are:

- Uses a  ``src/library`` layout.
- Uses a ``setup.py`` file for project configuration.
- Includes a ``pyproject.toml`` for tools configuration.
- Includes ``doc/`` and ``tests/`` directories.
- All ``requirements_*.txt`` are contained in the base directory.

To create a new project using this template by running:

.. code-block:: text

    ansys-templates new pybasic

.. admonition:: Link to demo

    `ansys-templates/demo - pybasic <https://github.com/ansys/ansys-templates/tree/demo/pybasic>`_

pyansys
-------
This template renders to a basic Python project compliant with the latest
PyAnsys guidelines.

Main features of this package are:

- Uses Ansys namespace by creating a ``src/ansys/product/library``.
- Uses a ``setup.py`` file for project configuration.
- Includes a ``pyproject.toml`` for tools configuration.
- Includes ``doc/`` and ``tests/`` directories.
- Includes GitHub workflows (actions).
- All ``requirements_*.txt`` are contained in the base directory.

To create a new project using this template, run:

.. code-block:: text

    ansys-templates new pyansys

.. admonition:: Link to demo

    `ansys-templates/demo - pyansys <https://github.com/ansys/ansys-templates/tree/demo/pyansys>`_

pyansys-advanced
----------------
This template renders to a basic Python project compliant with the latest
PyAnsys guidelines and the most modern techniques in Python packaging.

Main features of this package are:

- Uses Ansys namespace by creating a ``src/ansys/product/library``.
- Includes a ``pyproject.toml`` for project and tools configuration.
- Allows for the selection of the build-system between `flit`_, `poetry`_ or `setuptools`_.
- Includes ``doc/`` and ``tests/``.
- Includes GitHub workflows (actions).
- All ``requirements_*.txt`` are contained in a ``requirements_/`` directory.
- Includes a ``tox.ini`` file.

To create a new project using this template, run:

.. code-block:: text

    ansys-templates new pyansys-advanced

.. admonition:: Link to demo

    The there are three demo branches depending on your build-system.

    * `ansys-templates/demo - pyansys-advanced-flit <https://github.com/ansys/ansys-templates/tree/demo/pyansys-advanced-flit>`_
    * `ansys-templates/demo - pyansys-advanced-poetry <https://github.com/ansys/ansys-templates/tree/demo/pyansys-advanced-poetry>`_
    * `ansys-templates/demo - pyansys-advanced-setuptools <https://github.com/ansys/ansys-templates/tree/demo/pyansys-advanced-setuptools>`_

pyansys-openapi-client
----------------------
Create an OpenAPI Client Package project compliant with PyAnsys guidelines.

Main features of this package are:

- Includes GitHub workflows for generating, building and testing the library.
- Customizable ``pom.xml`` file.
- Customizable ``.m2/settings.xml`` file.

To create a new project using this template, run:

.. code-block:: text

    ansys-templates new pyansys-openapi-client

.. admonition:: Link to demo

    Demo unavailable at the moment.

pyace
-----
This template renders to a basic Python project compliant with the latest
ACE guidelines.

Main features of this package are:

- Uses a ``src/`` layout.
- Includes a ``pyproject.toml`` for project and tools configuration.
- Allows for the selection of the build-system between `flit`_, `poetry`_ or `setuptools`_.
- Includes ``doc/`` and ``tests/``.
- Allows CI platform selection between GitHub and Azure DevOps.
- All ``requirements_*.txt`` are contained in a ``requirements_/`` directory.
- Includes a ``tox.ini`` file.
- Ability to integrate Docker within the project.

To create a new project using this template, run:

.. code-block:: text

    ansys-templates new pyace-pkg

.. admonition:: Link to demo

    `ansys-templates/demo - pyace-pkg <https://github.com/ansys/ansys-templates/tree/demo/pyace-pkg>`_

pyace-fast
----------
This template renders to a basic Python project compliant with the latest
ACE guidelines and focused on `FastAPI`_ development:

Main features of this package are:

- Focused on `FastAPI`_ development.
- Uses a ``src/`` layout.
- Includes a ``pyproject.toml`` for project and tools configuration.
- Allows for the selection of the build-system between `flit`_, `poetry`_ or `setuptools`_.
- Includes ``doc/`` and ``tests/``.
- Allows CI platform selection between GitHub and Azure DevOps.
- All ``requirements_*.txt`` are contained in a ``requirements_/`` directory.
- Includes a ``tox.ini`` file.
- Ability to integrate Docker within the project.

To create a new project using this template, run:
.. code-block:: text

    ansys-templates new pyace-fast

.. admonition:: Link to demo

    `ansys-templates/demo - pyace-fast <https://github.com/ansys/ansys-templates/tree/demo/pyace-fast>`_

pyace-flask
-----------
This template renders to a basic Python project compliant with the latest
ACE guidelines and focused on `Flask`_ development:

Main features of this package are:

- Focused on `Flask`_ development.
- Uses a ``src/`` layout.
- Includes a ``pyproject.toml`` for project and tools configuration.
- Allows for the selection of the build-system between `flit`_, `poetry`_ or `setuptools`_.
- Includes ``doc/`` and ``tests/``.
- Allows CI platform selection between GitHub and Azure DevOps.
- All ``requirements_*.txt`` are contained in a ``requirements_/`` directory.
- Includes a ``tox.ini`` file.
- Ability to integrate Docker within the project.

To create a new project using this template, run:

.. code-block:: text

    ansys-templates new pyace-flask

.. admonition:: Link to demo

    `ansys-templates/demo - pyace-flask <https://github.com/ansys/ansys-templates/tree/demo/pyace-flask>`_

pyace-grpc
----------
This template renders to a basic Python project compliant with the latest
ACE guidelines and focused on `GRPC`_ development:

Main features of this package are:

- Focused on `GRPC`_ development.
- Uses a ``src/`` layout.
- Includes a ``pyproject.toml`` for project and tools configuration.
- Allows for the selection of the build-system between `flit`_, `poetry`_ or `setuptools`_.
- Includes ``doc/`` and ``tests/``.
- Allows CI platform selection between GitHub and Azure DevOps.
- All ``requirements_*.txt`` are contained in a ``requirements_/`` directory.
- Includes a ``tox.ini`` file.
- Ability to integrate Docker within the project.

To create a new project using this template, run:
.. code-block:: text

    ansys-templates new pyace-grpc

.. admonition:: Link to demo

    `ansys-templates/demo - pyace-grpc <https://github.com/ansys/ansys-templates/tree/demo/pyace-grpc>`_

solution
--------
This template renders to a Python project compliant with the latest Solutions
Application guidelines:

Main features of this package are:

- The build system is imposed to be ``poetry``.
- Uses a ``src/`` layout.
- Includes a ``pyproject.toml`` for project and tools configuration.
- Includes ``doc/`` and ``tests/``.
- Includes GitHub workflows (actions).
- Includes a ``tox.ini`` file.

To create a new project using this template, run:
.. code-block:: text

    ansys-templates new solution

.. admonition:: Link to demo

    `ansys-templates/demo - solution <https://github.com/ansys/ansys-templates/tree/demo/solution>`_

.. Links and references

.. _flit: https://flit.pypa.io/en/latest/
.. _poetry: https://python-poetry.org/
.. _setuptools: https://setuptools.pypa.io/en/latest/index.html
.. _fastapi: https://fastapi.tiangolo.com/
.. _flask: https://flask.palletsprojects.com/en/latest
.. _grpc: https://grpc.io/
