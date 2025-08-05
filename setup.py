"""Project installation script."""

from setuptools import find_namespace_packages, setup

setup(
    name="project-library",
    version="0.1.dev0",
    url="https://github.com/ansys/project",
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
    description="A my_company Python project for my_company library",
    long_description=open("README.rst").read(),
    install_requires=["importlib-metadata >=4.0"],
    python_requires=">=3.12",
    packages=find_namespace_packages(where="src"),
    package_dir={"": "src"},
)
