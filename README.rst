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

Ansys templates
===============
|ansys| |python| |pypi| |GH-CI| |codecov| |MIT| |black|

.. |ansys| image:: https://img.shields.io/badge/Ansys-ffc107.svg?labelColor=black&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAABDklEQVQ4jWNgoDfg5mD8vE7q/3bpVyskbW0sMRUwofHD7Dh5OBkZGBgW7/3W2tZpa2tLQEOyOzeEsfumlK2tbVpaGj4N6jIs1lpsDAwMJ278sveMY2BgCA0NFRISwqkhyQ1q/Nyd3zg4OBgYGNjZ2ePi4rB5loGBhZnhxTLJ/9ulv26Q4uVk1NXV/f///////69du4Zdg78lx//t0v+3S88rFISInD59GqIH2esIJ8G9O2/XVwhjzpw5EAam1xkkBJn/bJX+v1365hxxuCAfH9+3b9/+////48cPuNehNsS7cDEzMTAwMMzb+Q2u4dOnT2vWrMHu9ZtzxP9vl/69RVpCkBlZ3N7enoDXBwEAAA+YYitOilMVAAAAAElFTkSuQmCC
   :target: https://github.com/ansys
   :alt: PyAnsys

.. |python| image:: https://img.shields.io/pypi/pyversions/ansys-templates?logo=pypi
   :target: https://pypi.org/project/ansys-templates/
   :alt: Python

.. |pypi| image:: https://img.shields.io/pypi/v/ansys-templates.svg?logo=python&logoColor=white
   :target: https://pypi.org/project/ansys-templates/
   :alt: PyPI

.. |codecov| image:: https://codecov.io/gh/ansys/ansys-templates/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/ansys/ansys-templates
   :alt: Codecov

.. |GH-CI| image:: https://github.com/ansys/ansys-templates/actions/workflows/ci.yml/badge.svg
   :target: https://github.com/ansys/ansys-templates/actions/workflows/ci.yml
   :alt: CH-CI

.. |MIT| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
   :alt: MIT

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg?style=flat
   :target: https://github.com/psf/black
   :alt: Black


The ``ansys-templates`` repository holds a collection of useful templates compliant
with PyAnsys guidelines. It also provides the ``ansys-templates`` command line tool
for interactively generating new projects based on previous templates.

The main advantages of using this tool are:

- Building process is fully interactive. There is no need to manually modify files.
- Output of the project can easily be customized during the rendering process.
- Generated projects are compliant with `PyAnsys Developer's Guidelines`_.

.. _PyAnsys Developer's Guidelines: https://dev.docs.pyansys.com/

For information on using this tool, see the `Ansys Templates Documentation`_.

.. _Ansys Templates Documentation: https://templates.ansys.com/

.. image:: https://github.com/ansys/ansys-templates/raw/main/doc/source/_static/basic_usage.gif


How to install
--------------
Users can install ``ansys-templates`` by running:

.. code-block:: text

    python -m pip install ansys-templates

The usage of `pipx`_ is encouraged too. See `installing ansys-templates using
pipx`_.

.. _pipx: https://pipx.pypa.io/stable/
.. _installing ansys-templates using pipx: https://templates.ansys.com/version/stable/getting_started/index.html#installing-pipx


Basic commands
--------------
The following commands are provided with ``ansys-templates``:

- ``ansys-templates --help``: lists information about the tool.
- ``ansys-templates list``: lists all available templates.
- ``ansys-templates new <template name>``: creates a new project from template.

Available templates
-------------------
Available templates in ``ansys-templates`` are:

- ``doc-project``: Create a documentation project using Sphinx.
- ``pybasic``: Create a basic Python Package.
- ``pyansys``: Create a PyAnsys Python Package project.
- ``pyansys-advanced``: Create an advanced PyAnsys Python Package project.
- ``pyansys-openapi-client``: Create an OpenAPI Client Package project.
- ``pyace``: Create a Python project for any method developers.
- ``pyace-flask``: Create a Flask project initialized for any developer.
- ``pyace-grpc``: Create gRPC project initialized for any developer.
- ``pyace-fast``: Create a FastAPI project initialized for any developer.
- ``solution``: Create a Solution based on the Solution Application Framework. **For Ansys Internal Use Only**


Template features
-----------------
The following table summarizes the main properties for each of the templates
available in ``ansys-templates``:

+-------------------------+-----------------------+-----------------+---------+----------+----------------+---------+
| Template                | setup.py              | pyproject.toml  | Actions | tox.ini  | requirements/  | Docker  |
+=========================+=======================+=================+=========+==========+================+=========+
| doc-project             |                       |                 |  ``X``  |  ``X``   |  ``X``         |         |
+-------------------------+-----------------------+-----------------+---------+----------+----------------+---------+
| pybasic                 | ``X``                 |                 |         |          |                |         |
+-------------------------+-----------------------+-----------------+---------+----------+----------------+---------+
| pyansys                 |  ``X``                |  ``X``          |  ``X``  |          |                |         |
+-------------------------+-----------------------+-----------------+---------+----------+----------------+---------+
| pyansys-advanced        |  ``X``                |  ``X``          |  ``X``  |  ``X``   |  ``X``         |         |
+-------------------------+-----------------------+-----------------+---------+----------+----------------+---------+
| pyansys-openapi-client  |                       |                 |         |          |                |         |
+-------------------------+-----------------------+-----------------+---------+----------+----------------+---------+
| pyace                   |  ``X``                |  ``X``          |  ``X``  |  ``X``   |  ``X``         |  ``X``  |
+-------------------------+-----------------------+-----------------+---------+----------+----------------+---------+
| pyace-fast              |  ``X``                |  ``X``          |  ``X``  |  ``X``   |  ``X``         |  ``X``  |
+-------------------------+-----------------------+-----------------+---------+----------+----------------+---------+
| pyace-flask             |  ``X``                |  ``X``          |  ``X``  |  ``X``   |  ``X``         |  ``X``  |
+-------------------------+-----------------------+-----------------+---------+----------+----------------+---------+
| pyace-grpc              |  ``X``                |  ``X``          |  ``X``  |  ``X``   |  ``X``         |  ``X``  |
+-------------------------+-----------------------+-----------------+---------+----------+----------------+---------+
| solution "*"            |                       |  ``X``          |  ``X``  |  ``X``   |  ``X``         |         |
+-------------------------+-----------------------+-----------------+---------+----------+----------------+---------+

.. warning::
    "*" This template is for **Ansys Internal Use Only**.

Demo branches
-------------
To have a better idea on how each template will look once it gets rendered, see
its corresponding demonstration branch.

* Demo branch for `doc-project`_
* Demo branch for `pybasic`_
* Demo branch for `pyansys`_
* Demo branch for `pyansys-advanced using flit`_
* Demo branch for `pyansys-advanced using poetry`_
* Demo branch for `pyansys-advanced using setuptools`_
* Demo branch for `pyace`_
* Demo branch for `pyace-fast`_
* Demo branch for `pyace-flask`_
* Demo branch for `pyace-grpc`_
* Demo branch for `solution`_
* Demo branch for `osl-solution`_


.. _doc-project: https://github.com/ansys/ansys-templates/tree/demo/doc-project
.. _pybasic: https://github.com/ansys/ansys-templates/tree/demo/pybasic
.. _pyansys: https://github.com/ansys/ansys-templates/tree/demo/pyansys
.. _pyansys-advanced using flit: https://github.com/ansys/ansys-templates/tree/demo/pyansys-advanced-flit
.. _pyansys-advanced using poetry: https://github.com/ansys/ansys-templates/tree/demo/pyansys-advanced-poetry
.. _pyansys-advanced using setuptools: https://github.com/ansys/ansys-templates/tree/demo/pyansys-advanced-setuptools
.. _pyace: https://github.com/ansys/ansys-templates/tree/demo/pyace-pkg
.. _pyace-fast: https://github.com/ansys/ansys-templates/tree/demo/pyace-fast
.. _pyace-flask: https://github.com/ansys/ansys-templates/tree/demo/pyace-flask
.. _pyace-grpc: https://github.com/ansys/ansys-templates/tree/demo/pyace-grpc
.. _solution: https://github.com/ansys/ansys-templates/tree/demo/solution
.. _osl-solution: https://github.com/ansys/ansys-templates/tree/demo/solution

