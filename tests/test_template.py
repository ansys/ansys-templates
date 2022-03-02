import pytest

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
def test_bake_project_with_build_system(cookies, tool):
    result = cookies.bake(
        extra_context={
            "product_name": PRODUCT_NAME,
            "product_name_slug": PRODUCT_NAME_SLUG,
            "library_name": LIBRARY_NAME,
            "library_name_slug": LIBRARY_NAME_SLUG,
            "project_name_slug": PROJECT_NAME_SLUG,
            "pkg_name": PKG_NAME,
            "version": VERSION,
            "short_description": SHORT_DESCRIPTION,
            "repository_url": REPOSITORY_URL,
            "requires_python": REQUIRES_PYTHON,
            "build_system": tool,
            "max_linelength": MAX_LINELENGTH,
        }
    )

    assert result.exit_code == 0, result.exception
    assert result.exception is None
    assert result.project_path.name == PROJECT_NAME_SLUG
    assert result.project_path.is_dir()

    files = [
        ".github/workflows/ci_cd.yml",
        ".gitignore",
        ".flake8",
        ".pre-commit-config.yaml",
        "LICENSE",
        "README.rst",
        "requirements/requirements_tests.txt",
        "requirements/requirements_doc.txt",
        "requirements/requirements_build.txt",
        "pyproject.toml" if tool != "setuptools" else "setup.py",
        "tox.ini",
    ]

    dirs = [
        ".github",
        ".github/workflows",
        "doc",
        "doc/source",
        "requirements",
        "src",
        "src/ansys/" + PRODUCT_NAME_SLUG,
        "src/ansys/" + PRODUCT_NAME_SLUG + "/" + LIBRARY_NAME_SLUG,
        "tests",
    ]

    for path in files:
        assert (result.project_path / path).is_file()
    for path in dirs:
        assert (result.project_path / path).is_dir()
