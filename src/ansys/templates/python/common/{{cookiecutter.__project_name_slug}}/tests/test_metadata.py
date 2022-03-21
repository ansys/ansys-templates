from {{cookiecutter.__pkg_namespace}} import __version__


def test_pkg_version():
    assert __version__ == "{{ cookiecutter.__version }}"
