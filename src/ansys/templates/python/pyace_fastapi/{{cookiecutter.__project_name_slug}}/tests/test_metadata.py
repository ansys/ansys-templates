from src import __version__


def test_pkg_version():
    assert __version__ == "{{ cookiecutter.__version }}"
