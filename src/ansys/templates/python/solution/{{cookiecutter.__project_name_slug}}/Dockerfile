FROM python:3.10-alpine as base

ARG SOLUTIONS_PRIVATE_PYPI_PAT

RUN apk add --no-cache build-base libffi libressl gcc python3-dev linux-headers

# TODO: get poetry version from pyproject file
RUN pip install --upgrade pip && \
    pip install poetry==1.5.1

RUN poetry config http-basic.solutions-private-pypi PAT ${SOLUTIONS_PRIVATE_PYPI_PAT}
RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock /app/
COPY src/ /app/src/
COPY README.rst /app/README.rst

WORKDIR /app

FROM base as my_solution_api

RUN poetry install

# We use glow_engine instead of my_solution_main as entrypoint because the latter also loads
# the UI python files, carrying their dash dependencies, even if only the API is launched.
ENTRYPOINT ["glow_engine", "api"]

{% if cookiecutter.with_dash_ui == "yes" %}
FROM my_solution_api as my_solution_ui

RUN poetry install --with ui

ENTRYPOINT ["glow_engine", "ui"]
{% endif %}