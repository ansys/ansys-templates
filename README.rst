PyAnsys library as cookiecutter template
========================================

This repository holds a `cookiecutter`_ template for
creating a Python library. The process is fully interactive and the rendered
project is compliant with the `PyAnsys Developer's guide`_.


Requirements
------------

Before creating your library, you will need to install `cookiecutter`_ via:

.. code:: bash

    python -m pip install cookiecutter


How to use
----------

Once you have installed `cookiecutter`_, you can create a new Python library by
calling this template using:

.. code:: bash

    cookiecutter gh:pyansys/pyansys-template

Previous command will ask you to introduce different data regarding your new
Python project. Some of these are already pre-defined but you can always change
their value:

- **product_name**: the name of Ansys product (i.e. Product).
- **product_name_slug**: product sanitized name (i.e. product).
- **library_name**: the name of the product library (i.e. Library).
- **library_name_slug**: library named sanitized (i.e. library).
- **project_name_slug**: the project's directory name (i.e. pyproduct-library).
- **pkg_name**: the name of the Python package/library (i.e. ansys-product-library).
- **version**: the version of the package/library (i.e. 0.1.dev0).
- **short_description**: a short description of the purpose/goal of the project.
- **repository_url**: link to the repository where the source code will be hosted.
- **requires_python**: choose the minimum required Python version among 3.7, 3.8, 3.9 or 3.10.
- **build_system**: choose the build system among flit, poetry or setuptools.
- **max_linelength**: maximum number of characters per line in the source code (i.e. 100).


How to contribute
-----------------

For developers, the requirements can be installed via:

.. code:: bash

    python -m pip install -r requirements/requirements_dev.txt

The coding style checks and unit tests are executed via `tox`_. Simply execute:

.. code:: bash

    tox

and all the environments (style and tests) will be checked.


.. LINKS AND REFERENCES
.. _cookiecutter: https://cookiecutter.readthedocs.io/en/latest/
.. _PyAnsys Developer's guide: https://dev.docs.pyansys.com/
.. _tox: https://tox.wiki/
