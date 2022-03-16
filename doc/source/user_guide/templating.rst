How to Add a New Template
=========================

You can easily add new templates to ``ansys-templates``. Before adding a new
template, it is important that you read the CONTRIBUTING section.


Understanding the templates directory
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


Therefore, you must check if there is already a family for the template you want
to add or you need to create one.


Adding a new family of templates
--------------------------------

Start by creating a new directory in ``src/ansys/templates/`` with the name of
the new family of templates. For example, let us name it ``src/ansys/templates/new_family``:

.. code:: bash

   src/ansys/templates/
   │
   └── new_family/
       └── common/
          ├── cookiecutter.json
          └── {{cookiecutter.__project_name_slug}}
              └── ...

Inside this new family, you will need to create at least two different files:

- A ``cookiecutter.json`` file for specifying the minimum required variables for
  any of the templates of the family to work. You must use cookiecutter private
  variables in here.

- A ``common/{{cookiecutter.__project_name_slug}}/`` directory. This directory
  will contain all the common files which will be copied to any of the templates
  of your family when rendering those. You can later remove non-desired files if
  if needed.


Adding a new template to a family
---------------------------------
