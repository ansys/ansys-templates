"""Installation file for ansys-mapdl-core."""

from setuptools import find_namespace_packages, setup

setup(
    name="{{ cookiecutter.__pkg_name }}",
    packages=find_namespace_packages(where="src", include="ansys*"),
    package_dir={"": "src"},
    version="{{ cookiecutter.version }}",
    description="{{ cookiecutter.short_description }}",
    long_description=open("README.rst").read(),
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    url="{{ cookiecutter.repository_url }}",
    python_requires=">={{ cookiecutter.requires_python }}",
    install_requires=["importlib-metadata >=4.0"],
)
