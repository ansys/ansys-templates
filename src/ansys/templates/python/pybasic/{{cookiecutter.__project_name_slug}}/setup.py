from setuptools import setup, find_packages

setup(
    name="{{ cookiecutter.__pkg_name }}",
    version="{{ cookiecutter.__version }}",
    description="{{ cookiecutter.__short_description }}",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)
