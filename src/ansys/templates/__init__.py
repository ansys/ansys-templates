# Copyright (C) 2022 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
PyAnsys Templates.

A collection of interactive templates for building Python projects from scratch
according to PyAnsys guidelines.
"""

try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata

__version__ = importlib_metadata.version(__name__.replace(".", "-"))

AVAILABLE_TEMPLATES_AND_DESCRIPTION = {
    "doc-project": "Create a documentation project using Sphinx.",
    "pybasic": "Create a basic Python Package.",
    "pyansys": "Create a PyAnsys Python Package project.",
    "pyansys-advanced": "Create an advanced PyAnsys Python Package project.",
    "pyansys-openapi_client": "Create an OpenAPI Client Package project.",
    "pyace": "Create a Python project for any method developers.",
    "pyace-flask": "Create a Flask project initialized for any developer.",
    "pyace-grpc": "Create gRPC project initialized for any developer.",
    "pyace-fast": "Create a FastAPI project initialized for any developer.",
    "solution": "[Ansys Internal Use Only] Create a solution based on SAF.",
}
"""A list holding all available templates names."""
