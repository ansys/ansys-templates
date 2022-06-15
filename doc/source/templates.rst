Available templates
===================

All the available templates in ``ansys-templates`` are listed below these lines.
Their main features are explained so users can select the template which fits
their needs.

For quick-reference, the following table provides an overview of the main
capabilities and features of each template:

+-------------------------+-----------------------+-----------------+---------+----------+----------------+---------+
| Template                | setup.py              | pyproject.toml  | Actions | tox.ini  | requirements/  | Docker  |
+=========================+=======================+=================+=========+==========+================+=========+
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

.. note::

   In the ``demo/`` branches of the repository you can find rendered versions
   for each one of the templates. Take a look to these branches for having a
   better idea on the final project layout.


``pybasic`` template
--------------------
This template renders to a basic Python project. It does not follow the Ansys
namespace, meaning that a ``src/library/`` layout is produced instead of the
``src/ansys/product/library`` one. 

Main features of this package are:

- Uses a  ``src/library`` layout.
- Uses a ``setup.py`` file for project configuration.
- Includes a ``pyproject.toml`` for tools configuration.
- Includes ``doc/`` and ``tests/`` directories.
- All ``requirements_*.txt`` are contained in the base directory.


.. admonition:: Link to demo

    https://github.com/pyansys/ansys-templates/tree/demo/pybasic


``pyansys`` template
--------------------
This template renders to a basic Python project compliant with the latest
PyAnsys guidelines. 

Main features of this package are:

- Uses Ansys namespace by creating a ``src/ansys/product/library``.
- Uses a ``setup.py`` file for project configuration.
- Includes a ``pyproject.toml`` for tools configuration.
- Includes ``doc/`` and ``tests/`` directories.
- Includes GitHub workflows (actions).
- All ``requirements_*.txt`` are contained in the base directory.

.. admonition:: Link to demo

    https://github.com/pyansys/ansys-templates/tree/demo/pyansys


``pyansys-advanced`` template
-----------------------------
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

.. admonition:: Link to demo

    https://github.com/pyansys/ansys-templates/tree/demo/pyansys-advanced


``pyansys-openapi-client`` template
-----------------------------------
Create an OpenAPI Client Package project compliant with PyAnsys guidelines.

Main features of this package are:

- Includes GitHub workflows for generating, building and testing the library.
- Customizable ``pom.xml`` file.
- Customizable ``.m2/settings.xml`` file.


.. admonition:: Link to demo

    This project does not have a demo branch.


``pyace`` template
------------------
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

.. admonition:: Link to demo

    https://github.com/pyansys/ansys-templates/tree/demo/pyace-pkg


``pyace-fast`` template
-----------------------
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

.. admonition:: Link to demo

    https://github.com/pyansys/ansys-templates/tree/demo/pyace-fast


``pyace-flask`` template
------------------------
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

.. admonition:: Link to demo

    https://github.com/pyansys/ansys-templates/tree/demo/pyace-flask


``pyace-grpc`` template
-----------------------
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

.. admonition:: Link to demo

    https://github.com/pyansys/ansys-templates/tree/demo/pyace-grpc


.. Links and references

.. _flit: https://flit.pypa.io/en/latest/
.. _poetry: https://python-poetry.org/
.. _setuptools: https://setuptools.pypa.io/en/latest/index.html
.. _fastapi: https://fastapi.tiangolo.com/
.. _flask: https://flask.palletsprojects.com/en/latest
.. _grpc: https://grpc.io/
