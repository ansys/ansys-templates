.. _ref_release_notes:

Release notes
#############

This document contains the release notes for the project.

.. vale off

.. towncrier release notes start

`5.2.0 <https://github.com/ansys/ansys-templates/releases/tag/v5.2.0>`_ - April 08, 2025
========================================================================================

.. tab-set::


  .. tab-item:: Documentation

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - chore: update CHANGELOG for v5.1.0
          - `#538 <https://github.com/ansys/ansys-templates/pull/538>`_


`5.1.0 <https://github.com/ansys/ansys-templates/releases/tag/v5.1.0>`_ - April 08, 2025
========================================================================================

.. tab-set::


  .. tab-item:: Miscellaneous

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Add method to detect activated venv.
          - `#520 <https://github.com/ansys/ansys-templates/pull/520>`_

        * - fix: replace move by copy method to enable overwrite.
          - `#522 <https://github.com/ansys/ansys-templates/pull/522>`_

        * - Add token validity check.
          - `#528 <https://github.com/ansys/ansys-templates/pull/528>`_

        * - Use more recent version of dash-super-components
          - `#530 <https://github.com/ansys/ansys-templates/pull/530>`_

        * - [new solution] Support for python 3.12
          - `#531 <https://github.com/ansys/ansys-templates/pull/531>`_

        * - [new-solution] runtime error in the UI container
          - `#533 <https://github.com/ansys/ansys-templates/pull/533>`_


  .. tab-item:: Documentation

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - chore: update CHANGELOG for v5.0.0
          - `#517 <https://github.com/ansys/ansys-templates/pull/517>`_

        * - fix PYPI PAT in README
          - `#527 <https://github.com/ansys/ansys-templates/pull/527>`_


  .. tab-item:: Maintenance

    .. list-table::
        :header-rows: 0
        :widths: auto

        * - Build(deps): Bump ansys/actions from 7 to 8
          - `#507 <https://github.com/ansys/ansys-templates/pull/507>`_

        * - feat: Add .gitattributes file
          - `#536 <https://github.com/ansys/ansys-templates/pull/536>`_


`5.0.0 <https://github.com/ansys/ansys-templates/releases/tag/v5.0.0>`_ - 2024-12-09
====================================================================================

Fixed
^^^^^

- fix: contribut**** files `#509 <https://github.com/ansys/ansys-templates/pull/509>`_


Miscellaneous
^^^^^^^^^^^^^

- Update solution template `#516 <https://github.com/ansys/ansys-templates/pull/516>`_


Documentation
^^^^^^^^^^^^^

- chore: update CHANGELOG for v4.0.0 `#503 <https://github.com/ansys/ansys-templates/pull/503>`_


Maintenance
^^^^^^^^^^^

- Update dev version. `#504 <https://github.com/ansys/ansys-templates/pull/504>`_
- Add configuration file for containerized deployment. `#512 <https://github.com/ansys/ansys-templates/pull/512>`_

`4.0.0 <https://github.com/ansys/ansys-templates/releases/tag/v4.0.0>`_ - 2024-08-19
====================================================================================

Fixed
^^^^^

- fix: updating poetry.lock before local wheels are used in solution template `#495 <https://github.com/ansys/ansys-templates/pull/495>`_
- maint: update theme version, actions and logo `#501 <https://github.com/ansys/ansys-templates/pull/501>`_


Dependencies
^^^^^^^^^^^^

- Build(deps-dev): Bump pytest-cov from 4.1.0 to 5.0.0 `#457 <https://github.com/ansys/ansys-templates/pull/457>`_
- Build(deps): Bump pytest from 8.2.1 to 8.2.2 `#489 <https://github.com/ansys/ansys-templates/pull/489>`_
- Build(deps): Bump ansys-sphinx-theme from 0.16.0 to 0.16.5 `#490 <https://github.com/ansys/ansys-templates/pull/490>`_


Miscellaneous
^^^^^^^^^^^^^

- Replace AWC Tree by Dash Tree in the default UI mode of the solution template `#498 <https://github.com/ansys/ansys-templates/pull/498>`_
- Remove pydantic constraint. `#502 <https://github.com/ansys/ansys-templates/pull/502>`_


Documentation
^^^^^^^^^^^^^

- chore: update CHANGELOG for v3.0.0 `#488 <https://github.com/ansys/ansys-templates/pull/488>`_


Maintenance
^^^^^^^^^^^

- Build(deps): Bump peter-evans/create-or-update-comment from 3 to 4 `#432 <https://github.com/ansys/ansys-templates/pull/432>`_
- Build(deps): Bump ansys/actions from 6 to 7 `#499 <https://github.com/ansys/ansys-templates/pull/499>`_
- Update dependencies. `#500 <https://github.com/ansys/ansys-templates/pull/500>`_

`3.0.0 <https://github.com/ansys/ansys-templates/releases/tag/v3.0.0>`_ - 2024-06-04
====================================================================================

Added
^^^^^

- feat: update CLI option for creating a Dash UI using AWC as well `#477 <https://github.com/ansys/ansys-templates/pull/477>`_


Changed
^^^^^^^

- chore: update CHANGELOG for v2.1.0 `#473 <https://github.com/ansys/ansys-templates/pull/473>`_
- maint: bump main dev version `#474 <https://github.com/ansys/ansys-templates/pull/474>`_
- Maintenance/update solution template `#484 <https://github.com/ansys/ansys-templates/pull/484>`_


Fixed
^^^^^

- fix: update pydocstyle in ``pyproject.toml`` file `#478 <https://github.com/ansys/ansys-templates/pull/478>`_
- fix: run tests with specified python-version in CI `#480 <https://github.com/ansys/ansys-templates/pull/480>`_
- fix: change socio-economic to socioeconomic for codespell v2.3.0 `#485 <https://github.com/ansys/ansys-templates/pull/485>`_
- fix: suppress ``autosectionlabel`` warning for ``changelog`` file `#487 <https://github.com/ansys/ansys-templates/pull/487>`_


Dependencies
^^^^^^^^^^^^

- Build(deps): Bump ansys-sphinx-theme from 0.14.1 to 0.16.0 `#475 <https://github.com/ansys/ansys-templates/pull/475>`_
- Build(deps): Bump pytest from 8.1.1 to 8.2.1 `#479 <https://github.com/ansys/ansys-templates/pull/479>`_


Miscellaneous
^^^^^^^^^^^^^

- Update ansys saf portal version `#472 <https://github.com/ansys/ansys-templates/pull/472>`_
- feat: Add devcontainer config for codespaces `#481 <https://github.com/ansys/ansys-templates/pull/481>`_
- docs: update authors file `#482 <https://github.com/ansys/ansys-templates/pull/482>`_

`2.1.0 <https://github.com/ansys/ansys-templates/releases/tag/v2.1.0>`_ - 2024-05-14
====================================================================================

Changed
^^^^^^^

- chore: update templates `#471 <https://github.com/ansys/ansys-templates/pull/471>`_
