from ansys.{{cookiecutter.product_name_slug}} import {{ cookiecutter.library_name_slug }}


def test_pkg_version():
    assert {{ cookiecutter.library_name_slug }}.__version__ == "{{ cookiecutter.version }}"
