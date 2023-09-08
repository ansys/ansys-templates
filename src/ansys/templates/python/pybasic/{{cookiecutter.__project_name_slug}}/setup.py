from setuptools import setup, find_packages

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
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)
