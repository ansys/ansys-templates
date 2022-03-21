{{ cookiecutter.__project_name_slug }}
{{ '=' * (cookiecutter.__project_name_slug | length) }}

{{ cookiecutter.__short_description }}


How to install
--------------

At least two installation modes are provided: user and developer.

For users
^^^^^^^^^

User installation can be performed by running:

.. code:: bash

    python -m pip install {{ cookiecutter.__pkg_name }}

For developers
^^^^^^^^^^^^^^

Before contributing to the project, please refer to the `PyAnsys Developer's
guide`_. You will need to follow these steps:

1. Start by cloning this repository:

    .. code:: bash

        git clone {{ cookiecutter.repository_url }}

2. Create a fresh-clean Python environment and activate it. Refer to the
   official `venv`_ documentation if you require further information:

    .. code:: bash

        # Create a virtual environment
        python -m venv .venv

        # Activate it in a Linux environment
        python -m venv .venv && source .venv/bin/activate

        # Activate it in a Windows CMD environment
        source .venv\Scripts\activate.bat

        # Activate it in a Windows Powershell environment
        source .venv\Scripts\Activate.ps1


3. Make sure you have the latest version of `pip`_:

    .. code:: bash

        python -m pip install -U pip

4. Install the project in editable mode:

    .. code:: bash
    
        python -m pip install --editable {{ cookiecutter.__pkg_name }}

5. Install additional requirements (if needed):

     .. code:: bash

        python -m pip install -r requirements/requirements_build.txt
        python -m pip install -r requirements/requirements_doc.txt
        python -m pip install -r requirements/requirements_tests.txt


6. Finally, verify your development installation by running:

    .. code:: bash
        
        python -m pip install -r requirements/requirements_tests.txt
        pytest tests -vv


Style and Testing
-----------------

If required, you can always call the style commands (`black`_, `isort`_,
`flake8`_...) or unit testing ones (`pytest`_) from the command line. However,
this does not guarantee that your project is being tested in an isolated
environment, which is another reason to use tools like `tox`_.


Documentation
-------------

For building documentation, you can either run the usual rules provided in the
`Sphinx`_ Makefile, such us:

.. code:: bash

    python -m pip install -r requirements/requirements_doc.txt
    make -C doc/ html

    # optionally view the generated documentation (on linux) with
    your_browser_name doc/html/index.html


Distributing
------------

If you would like to create either source or wheel files, start by installing
the building requirements:

.. code:: bash

    python -m pip install -r requirements/requirements_build.txt

Then, you can execute:

    .. code:: bash

        python -m build
        python -m twine check dist/*


.. LINKS AND REFERENCES
.. _black: https://github.com/psf/black
.. _flake8: https://flake8.pycqa.org/en/latest/
.. _isort: https://github.com/PyCQA/isort
.. _PyAnsys Developer's guide: https://dev.docs.pyansys.com/
.. _pre-commit: https://pre-commit.com/
.. _pytest: https://docs.pytest.org/en/stable/
.. _Sphinx: https://www.sphinx-doc.org/en/master/
.. _pip: https://pypi.org/project/pip/
.. _tox: https://tox.wiki/
.. _venv: https://docs.python.org/3/library/venv.html
