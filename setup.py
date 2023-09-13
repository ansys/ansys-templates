from setuptools import setup, find_packages

setup(
    name="pybasic",
    version="0.1.dev0",
    url="https://platform.domain/organization/pybasic",
    author="ANSYS, Inc.",
    author_email="pyansys.support@ansys.com",
    maintainer="PyAnsys developers",
    maintainer_email="pyansys.maintainers@ansys.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license="MIT",
    license_file="LICENSE",
    description="A basic python package",
    long_description=open("README.rst").read(),
    install_requires=["importlib-metadata >=4.0"],
    python_requires=">=3.7",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)
