"""Project installation script."""

from setuptools import find_namespace_packages, setup

setup(
    name="{{ cookiecutter.__pkg_name }}",
    version="{{ cookiecutter.__version }}",
    url="{{ cookiecutter.__repository_url }}",
    author="ANSYS, Inc.",
    author_email="pyansys.support@ansys.com",
    maintainer="PyAnsys developers",
    maintainer_email="pyansys.core@ansys.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license="MIT",
    license_file="LICENSE",
    description="{{ cookiecutter.__short_description }}",
    long_description=open("README.rst").read(),
    install_requires=["importlib-metadata >=4.0"],
    python_requires=">={{ cookiecutter.__requires_python }}",
    {%- if cookiecutter.__is_pyansys == "True" %}
    packages=find_namespace_packages(where="src", include="ansys*"),
    {%- else %}
    packages=find_namespace_packages(where="src"),
    {%- endif %}
    package_dir={"": "src"},
)
