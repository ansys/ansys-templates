from ansys.{{cookiecutter.__product_name_slug}} import {{ cookiecutter.__library_name_slug }}


def test_pkg_version():
    assert {{ cookiecutter.__library_name_slug }}.__version__ == "{{ cookiecutter.version }}"
