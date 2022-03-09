from pathlib import Path

from cookiecutter.main import cookiecutter
import pytest

from ansys.templates.paths import PYPKG_TEMPLATE_PATH

PRODUCT_NAME = "Product"
PRODUCT_NAME_SLUG = PRODUCT_NAME.lower().replace(" ", "-").replace("_", "-")
LIBRARY_NAME = "Library"
LIBRARY_NAME_SLUG = LIBRARY_NAME.lower().replace(" ", "-").replace("_", "-")
PROJECT_NAME_SLUG = f"py{PRODUCT_NAME_SLUG}-{LIBRARY_NAME_SLUG}"
PKG_NAME = f"ansys-{PRODUCT_NAME_SLUG}-{LIBRARY_NAME_SLUG}"
VERSION = "0.1.dev0"
SHORT_DESCRIPTION = f"A Python wrapper for Ansys {PRODUCT_NAME} {LIBRARY_NAME}"
REPOSITORY_URL = f"https://github.com/pyansys/{PROJECT_NAME_SLUG}"
REQUIRES_PYTHON = "3.7"
MAX_LINELENGTH = "100"


@pytest.mark.parametrize("tool", ["flit", "poetry", "setuptools"])
def test_bake_project_with_build_system(tmpdir, tool):

    # Bake the project in the desired output directory
    cookiecutter(
        template=str(PYPKG_TEMPLATE_PATH),
        output_dir=str(tmpdir),
        no_input=True,
        extra_context={
            "product_name": PRODUCT_NAME,
            "__product_name_slug": PRODUCT_NAME_SLUG,
            "library_name": LIBRARY_NAME,
            "__library_name_slug": LIBRARY_NAME_SLUG,
            "__project_name_slug": PROJECT_NAME_SLUG,
            "__pkg_name": PKG_NAME,
            "version": VERSION,
            "short_description": SHORT_DESCRIPTION,
            "repository_url": REPOSITORY_URL,
            "requires_python": REQUIRES_PYTHON,
            "build_system": tool,
            "max_linelength": MAX_LINELENGTH,
        },
    )

    doc_files = [
        "doc/make.bat",
        "doc/Makefile",
        "doc/source/conf.py",
        "doc/source/index.rst",
        "doc/source/_static/README.md",
        "doc/source/_templates/README.md",
        "doc/source/_templates/sidebar-nav-bs.html",
    ]

    dot_files = [
        ".flake8",
        ".gitignore",
        ".pre-commit-config.yaml",
    ]

    github_files = [
        ".github/workflows/ci_cd.yml",
    ]

    requirements_files = [
        "requirements/requirements_tests.txt",
        "requirements/requirements_doc.txt",
        "requirements/requirements_build.txt",
    ]

    src_files = [
        f"src/ansys/{PRODUCT_NAME_SLUG}/{LIBRARY_NAME_SLUG}/__init__.py",
    ]

    tests_files = [
        "tests/test_metadata.py",
    ]

    basedir_files = [
        "LICENSE",
        "README.rst",
        "pyproject.toml" if tool != "setuptools" else "setup.py",
        "tox.ini",
    ]

    all_files = (
        basedir_files
        + src_files
        + doc_files
        + tests_files
        + requirements_files
        + dot_files
        + github_files
    )

    all_dirs = [
        ".github",
        ".github/workflows",
        "doc",
        "doc/source",
        "doc/source/_static",
        "doc/source/_templates",
        "requirements",
        "src",
        "src/ansys/" + PRODUCT_NAME_SLUG,
        "src/ansys/" + PRODUCT_NAME_SLUG + "/" + LIBRARY_NAME_SLUG,
        "tests",
    ]

    for filename in all_files:
        assert (Path(tmpdir) / PROJECT_NAME_SLUG / filename).is_file()

    for dirname in all_dirs:
        assert (Path(tmpdir) / PROJECT_NAME_SLUG / dirname).is_dir()
