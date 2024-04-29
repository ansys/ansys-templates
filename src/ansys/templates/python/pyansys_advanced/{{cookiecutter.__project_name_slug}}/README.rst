Py{{ cookiecutter.product_name }} {{ cookiecutter.library_name }}
{{ '=' * (cookiecutter.__project_name_slug | length) }}
|pyansys| |python| |pypi| |GH-CI| |codecov| |MIT| |black|

.. |pyansys| image:: https://img.shields.io/badge/Py-Ansys-ffc107.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAABDklEQVQ4jWNgoDfg5mD8vE7q/3bpVyskbW0sMRUwofHD7Dh5OBkZGBgW7/3W2tZpa2tLQEOyOzeEsfumlK2tbVpaGj4N6jIs1lpsDAwMJ278sveMY2BgCA0NFRISwqkhyQ1q/Nyd3zg4OBgYGNjZ2ePi4rB5loGBhZnhxTLJ/9ulv26Q4uVk1NXV/f///////69du4Zdg78lx//t0v+3S88rFISInD59GqIH2esIJ8G9O2/XVwhjzpw5EAam1xkkBJn/bJX+v1365hxxuCAfH9+3b9/+////48cPuNehNsS7cDEzMTAwMMzb+Q2u4dOnT2vWrMHu9ZtzxP9vl/69RVpCkBlZ3N7enoDXBwEAAA+YYitOilMVAAAAAElFTkSuQmCC
   :target: https://docs.pyansys.com/
   :alt: PyAnsys

.. |python| image:: https://img.shields.io/pypi/pyversions/{{cookiecutter.__pkg_name}}?logo=pypi
   :target: https://pypi.org/project/{{cookiecutter.__pkg_name}}/
   :alt: Python

.. |pypi| image:: https://img.shields.io/pypi/v/{{cookiecutter.__pkg_name}}.svg?logo=python&logoColor=white
   :target: https://pypi.org/project/{{cookiecutter.__pkg_name}}
   :alt: PyPI

.. |codecov| image:: https://codecov.io/gh/ansys/{{cookiecutter.__project_name_slug}}/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/ansys/{{cookiecutter.__project_name_slug}}
   :alt: Codecov

.. |GH-CI| image:: https://github.com/ansys/{{cookiecutter.__project_name_slug}}/actions/workflows/ci_cd.yml/badge.svg
   :target: https://github.com/ansys/{{cookiecutter.__project_name_slug}}/actions/workflows/ci_cd.yml
   :alt: GH-CI

.. |MIT| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
   :alt: MIT

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg?style=flat
   :target: https://github.com/psf/black
   :alt: Black


Overview
--------

{{ cookiecutter.short_description }}

.. contribute_start

Installation
^^^^^^^^^^^^

You can use `pip <https://pypi.org/project/pip/>`_ to install Py{{ cookiecutter.product_name }} {{ cookiecutter.library_name }}.

.. code:: bash

    pip install {{cookiecutter.__pkg_name}}

To install the latest development version, run these commands:

.. code:: bash

    git clone {{cookiecutter.__repository_url}}
    cd {{ cookiecutter.__project_name_slug }}
    pip install -e .

For more information, see `Getting Started`_.

Basic usage
^^^^^^^^^^^

This code shows how to import Py{{ cookiecutter.product_name }} {{ cookiecutter.library_name }} and use some basic capabilities:

.. code:: python

    print("Put sample code here")

For comprehensive usage information, see `Examples`_ in the `Py{{ cookiecutter.product_name }} {{ cookiecutter.library_name }} documentation`_.

Documentation and issues
^^^^^^^^^^^^^^^^^^^^^^^^
Documentation for the latest stable release of Py{{ cookiecutter.product_name }} {{ cookiecutter.library_name }} is hosted at `Py{{ cookiecutter.product_name }} {{ cookiecutter.library_name }} documentation`_.

In the upper right corner of the documentation's title bar, there is an option for switching from
viewing the documentation for the latest stable release to viewing the documentation for the
development version or previously released versions.

On the `Py{{ cookiecutter.product_name }} {{ cookiecutter.library_name }} Issues <{{cookiecutter.__repository_url}}/issues>`_ page,
you can create issues to report bugs and request new features. On the `Py{{ cookiecutter.product_name }} {{ cookiecutter.library_name }} Discussions
<{{cookiecutter.__repository_url}}/discussions>`_ page or the `Discussions <https://discuss.ansys.com/>`_
page on the Ansys Developer portal, you can post questions, share ideas, and get community feedback.

To reach the project support team, email `pyansys.core@ansys.com <mailto:pyansys.core@ansys.com>`_.


.. LINKS AND REFERENCES
.. _Getting Started: https://{{ cookiecutter.product_name }}.docs.pyansys.com/version/stable/getting_started/index.html
.. _Examples: https://{{ cookiecutter.product_name }}.docs.pyansys.com/version/stable/examples.html
.. _Py{{ cookiecutter.product_name }} {{ cookiecutter.library_name }} documentation: https://{{ cookiecutter.product_name }}.docs.pyansys.com/version/stable/index.html
