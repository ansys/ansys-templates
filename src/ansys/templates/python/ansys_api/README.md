### {{ cookiecutter.project_slug }} gRPC Interface Package

This Python package contains the auto-generated gRPC Python interface files for
{{ cookiecutter.product_name }}.


#### Installation

Provided that these wheels have been published to public PyPI, they can be
installed with:

```
pip install {{ cookiecutter.project_slug | lower }}
```

Otherwise, see the


#### Build

To build the gRPC packages, run:

```
pip install build
python -m build
```

This will create both the source distribution containing just the protofiles
along with the wheel containing the protofiles and build Python interface
files.

Note that the interface files are identical regardless of the version of Python
used to generate them, but the last pre-built wheel for ``grpcio~=1.17`` was
Python 3.7, so to improve your build time, use Python 3.7 when building the
wheel.


#### Manual Deployment

After building the packages, manually deploy them with:

```
pip install twine
twine upload dist/*
```

Note that this is automatically done through CI/CD.


#### Automatic Deployment

This repository contains GitHub CI/CD that enables the automatic building of
source and wheel packages for these gRPC Python interface files. By default,
these are built on PRs, the main branch, and on tags when pushing. Artifacts
are uploaded for each PR.

To publicly release wheels to PyPI, ensure your branch is up-to-date and then
push tags. For example, for the version ``v0.5.0``.

```bash
git tag v0.5.0
git push --tags
```
