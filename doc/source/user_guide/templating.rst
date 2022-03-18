How to Add a New Template
=========================

You can easily add new templates to ``ansys-templates``. Before adding a new
template, it is important that you read the CONTRIBUTING section.


Understanding the Templates Directory
-------------------------------------

All ``ansys-templates`` are collected inside the ``templates/`` directory, which
is included in the ``src/``. The ``templates/`` directory holds different
families of templates.

A ``family of templates`` is just a directory holding a ``common/`` folder and
various ``templates/``:

- The ``common/`` directory contains various resources which are common to all
  templates of a given family. This avoids duplication of files across templates.

- Each ``template/`` contains its own custom files.

.. code:: bash

   src/ansys/templates/
   │
   ├── family_0/
   │    ├── common/
   │    │   ├── cookiecutter.json
   │    │   └── {{cookiecutter.__project_name_slug}}
   │    │       └── ...
   │    ├── template_0/
   │    │   ├── cookiecutter.json
   │    │   └── {{cookiecutter.__project_name_slug}}
   │    │       └── ...
   │    ├── template_1/
   │    │   ├── cookiecutter.json
   │    │   └── {{cookiecutter.__project_name_slug}}
   │    │       └── ...
   │    └── template_N/
   │        ├── cookiecutter.json
   │        └── {{cookiecutter.__project_name_slug}}
   │            └── ...
   └── family_N/


Be sure to check if there is already a family for the template you want
to add or you need to create one.


Adding a New family of Templates
--------------------------------

Start by creating a new directory in ``src/ansys/templates/`` with the name of
the new family of templates. For example, let's name it ``src/ansys/templates/new_family``:

.. code:: bash

   src/ansys/templates/
   │
   └── new_family/
       └── common/
          ├── cookiecutter.json
          └── {{cookiecutter.__project_name_slug}}/
              └── ... # All these files will be included in each family template

Inside this new family, you will need to create at least two different files:

- A ``cookiecutter.json`` file for specifying the minimum required variables for
  any of the templates of the family to work. You must use cookiecutter private
  variables in here.

- A ``common/{{cookiecutter.__project_name_slug}}/`` directory. This directory
  contains all the typical files for a given family. All files in the
  ``common/{{cookiecutter.__project_name_slug}}`` directory will be copied to
  each template when rendering it.
  
.. note::

    You can later add a ``hooks/pos_gen_project.py`` file in the
    ``family/template/`` directory for removing non-desired files coming from
    the ``common/{{cookiecutter.__project_name_slug}}`` directory.


Adding a New Template to a Family
---------------------------------

To add a new template, start by creating a new template folder. For example, let's
name it ``src/ansys/templates/family_0/new_template``:

.. code:: bash

   src/ansys/templates/
   │
   └── family_0/
       ├── common/
       │   ├── cookiecutter.json
       │   └── {{cookiecutter.__project_name_slug}}
       │       └── ... # All these files will be included in new_template/
       └── new_template/
           ├── cookiecutter.json
           └── {{cookiecutter.__project_name_slug}}/
               └── ... # Custom template files

Inside the ``new_template/``, you will need to create at least two different files:

- A ``cookiecutter.json`` file for specifying the new template variables. You
  must override the ``common/cookiecutter.json`` variables too!

- A ``{{cookiecutter.__project_name_slug}}/`` directory. This directory must
  contain any additional files or directories you would like to include in your
  new template. Notice this folder will be combined with the
  ``common/{{cookiecutter.__project_name_slug}}/`` one.


Adding it to the CLI
^^^^^^^^^^^^^^^^^^^^

To have access to the template from the CLI (command line interface), you will
need to:

1. Include the named and description of the new template in the
   ``src/ansys/templates/__init__.py`` file under the
   ``AVAILABLE_TEMPLATES_AND_DESCRIPTION`` dictionary.

2. Add the path to the new template in ``src/ansys/templates/paths.py``. Include
   it in the ``TEMPLATE_PATH_FINDER`` dictionary too.

3. Create a command to expose the new template in the CLI:

   .. code:: python

       @new.command()
       def template_name():
           """Short description of the template."""
           bake_template(TEMPLATE_PATH_FINDER["pyansys"], os.getcwd())


Adding Unitary Tests
""""""""""""""""""""

Each template must have its own unit test script. The following namespace is
followed in order to organize the test suite:

- ``tests/tests_templates_family/test_template_family_name_of_template.py``

.. note::

   If you created a new family template, make sure to include tests for the
   ``family/common/`` directory too.

Expected common files should be included under a
``tests/tests_templates_family/conftest.py`` as a `pytest fixture`_. As an
example, consider the following code of a generic ``conftest.py`` file:

.. code::

    @pytest.fixture(scope="package")
    def family_common_files():

        # All expected common files
        basedir_files = ["README.rst", "LICENSE"]
        doc_files = [...]
        tests_files = [...]

        # Combine all files and export those to be accessible by the tests
        all_common_files = basedir_files + doc_files + tests_files
        return all_common_files


Add the Family to Tox envs
""""""""""""""""""""""""""

If you created a new faimly, make sure to add it to the [tox] set of
environments:

1. Look for the ``[testenv]`` section in the ``tox.ini`` file.
2. Within this section, look for the ``setenv`` variable.
3. Add the following line:

   .. code:: text

      family: PYTEST_MARKERS = -k "tests_templates_family"


Updating the CI
"""""""""""""""

Each family of templates is tested within its own `GitHub actions`_ workflow.
Therefore, you need to create a:

- ``.github/workflows/templates_family.yml``

.. note::

   To reduce the amount of CI jobs, templates are only tested under Linux based
   OS. If you require from any particular programming language, try to test the
   minimum and maximum supported versions/standards of the language. Avoid all
   the intermediate ones if possible.


Removing Undesired Files
------------------------

It is likely that you do not want some files coming from the ``common/``
directory to be included in your rendered template. You can take advantage of 
`cookiecutter hooks`_. 

Hooks are Python scripts which allow you to control the rendering process before
and after it has been executed. This way you can move or delete any files
included in the final rendered project. In order to use hooks, you need to
create a new directory named ``src/ansys/templates/new_family/new_template/hooks``.
Only two hooks are allowed:

- ``pre_gen_project.py``: executes before rendering process.
- ``post_gen_project.py``: executes after the rendering process.

.. warning::

   Both hooks are executed once cookiecutter context has been started. This
   implies that any file with a variable of the type {{ cookiecutter.some_var }}
   or Jinja2 syntax will not be rendered!


.. REFERENCES & LINKS

.. _cookiecutter hooks: https://cookiecutter.readthedocs.io/en/latest/advanced/hooks.html
.. _pytest fixture: https://docs.pytest.org/en/latest/explanation/fixtures.html
.. _GitHub actions: https://docs.github.com/en/actions
