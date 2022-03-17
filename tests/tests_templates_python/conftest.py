import pytest


@pytest.fixture(scope="package")
def python_common_files():
    doc_files = [
        "doc/make.bat",
        "doc/Makefile",
        "doc/source/conf.py",
        "doc/source/index.rst",
        "doc/source/_static/README.md",
        "doc/source/_templates/README.md",
        "doc/source/_templates/sidebar-nav-bs.html",
    ]

    basedir_files = [
        "README.rst",
        "requirements_build.txt",
        "requirements_tests.txt",
        "requirements_doc.txt",
        "LICENSE",
    ]

    tests_files = [
        "tests/test_metadata.py",
    ]

    all_files = doc_files + tests_files + basedir_files
    return all_files
