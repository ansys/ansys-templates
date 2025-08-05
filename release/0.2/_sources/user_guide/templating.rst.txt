How to Add a New Template
=========================

You can easily add new templates. However, before doing so, it is important that
you read the Contributing section.


Understanding the Templates Directory
-------------------------------------

In ``ansys-templates``, all templates are placed in ``src/ansys/templates/``.
The ``templates/`` directory contains different families of templates.

A `family of templates` is simply a directory with a ``common/`` folder and
various templates folders.

- The ``common/`` folder contains various resources that are common to all
  templates of a given family. This avoids duplication of files across templates.

- Each template folder contains its own set of custom files.

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
to add before creating a new one.


Adding a New Family of Templates
--------------------------------

Start by creating a new directory in ``src/ansys/templates/`` with the name of
the new family of templates. For example, create ``src/ansys/templates/new_family``:

.. code:: bash

   src/ansys/templates/
   │
   └── new_family/
       └── common/
          ├── cookiecutter.json
          └── {{cookiecutter.__project_name_slug}}/
              └── ... # All these files will be included in each family template

Inside this new family, you must create at least two different files:

- A ``cookiecutter.json`` file for specifying the minimum required variables for
  any of this family's templates to work. You must use cookie cutter private
  variables in this file.

- A ``common/{{cookiecutter.__project_name_slug}}/`` directory to contain all of
  the typical files for this family. All files in the ``common/{{cookiecutter.__project_name_slug}}``
  directory will be copied to each template when rendering it.
  
  
.. note::

    You can later add a ``hooks/post_gen_project.py`` file in the
    ``family/template/`` directory if you need to remove non-desired files coming from
    the ``common/{{cookiecutter.__project_name_slug}}`` directory.


Adding a New Template to a Family
---------------------------------

To add a new template to a family, first create a new template folder. For example,
``src/ansys/templates/family_0/new_template``:

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

Inside the ``new_template/`` directory, you must create at least two different files:

- A ``cookiecutter.json`` file for specifying variables for the new template and
  overriding ``common/cookiecutter.json`` variables.

- A ``{{cookiecutter.__project_name_slug}}/`` directory to contain any additional files or
  directories that you would like to include in your new template. The files in this directory
  will be combined with the files in the  ``common/{{cookiecutter.__project_name_slug}}/``
  directory.


Adding a New Template to the CLI
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To have access to a newly template from the CLI (command line interface), you must do
the following:

1. Include the name and description of the new template in the
   ``src/ansys/templates/__init__.py`` file under the
   ``AVAILABLE_TEMPLATES_AND_DESCRIPTION`` dictionary.

2. Add the path to the new template in ``src/ansys/templates/paths.py`` and in
   the ``TEMPLATE_PATH_FINDER`` dictionary.

3. Create a command to expose the new template in the CLI:

   .. code:: python

       @new.command()
       def template_name():
           """Short description of the template."""
           bake_template(TEMPLATE_PATH_FINDER["pyansys"], os.getcwd())


Adding Unit Tests
"""""""""""""""""

Each template must have its own unit test script. To organize the test suite,
the following namespace is followed:

- ``tests/tests_templates_family/test_template_family_name_of_template.py``

.. note::

   If you created a new family template, make sure to include tests for the
   ``family/common/`` directory too.

Expected common files should be defined in ``tests/tests_templates_family/conftest.py``
as a `pytest fixture`_. For example, consider the following code of a generic ``conftest.py``
file:

.. code:: python

    @pytest.fixture(scope="package")
    def family_common_files():

        # All expected common files
        basedir_files = ["README.rst", "LICENSE"]
        doc_files = [...]
        tests_files = [...]

        # Combine all files and export those to be accessible to the tests
        all_common_files = basedir_files + doc_files + tests_files
        return all_common_files


Add the Family to Tox envs
""""""""""""""""""""""""""

If you created a new family, you must add it to the [tox] set of
environments:

1. Look for the ``[testenv]`` section in the ``tox.ini`` file.
2. Within this section, look for the ``setenv`` variable.
3. Add the following line:

   .. code:: text

      family: PYTEST_MARKERS = -k "tests_templates_family"


Updating the CI
"""""""""""""""

Each family of templates is tested within its own `GitHub actions`_ workflow.
Therefore, you need to create a YML file for a new family:

- ``.github/workflows/templates_family.yml``

.. note::

   To reduce the amount of CI jobs, templates are only tested under Linux.
   If you require testing from a particular programming language, try to test the
   minimum and maximum supported versions of the language. Avoid all intermediate
   versions if possible.


Removing Undesired Files
------------------------

It is likely that there are some files coming from the ``common/``
directory that you do not want included in your rendered template. To exclude files,
you can take advantage of `cookiecutter hooks`_. 

Hooks are Python scripts that allow you to control the rendering process both before
and after the process is executed. With hooks, you can move or delete any files
included in the final rendered project.

To use hooks, you must create a new directory named ``src/ansys/templates/new_family/new_template/hooks``.
Only two hooks are allowed:

- ``pre_gen_project.py``: executes before rendering process.
- ``post_gen_project.py``: executes after the rendering process.

.. warning::

   Both hooks are executed once the cookiecutter context has been started. This
   implies that any file with a variable of the type ``{{ cookiecutter.some_var }}``
   or Jinja2 syntax will not be rendered.


.. REFERENCES & LINKS

.. _cookiecutter hooks: https://cookiecutter.readthedocs.io/en/latest/advanced/hooks.html
.. _pytest fixture: https://docs.pytest.org/en/latest/explanation/fixtures.html
.. _GitHub actions: https://docs.github.com/en/actions
