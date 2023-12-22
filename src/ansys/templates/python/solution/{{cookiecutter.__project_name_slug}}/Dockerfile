# === Base Stage ===
FROM python:3.10-alpine as base

# credentials will only be available during image built
ARG SOLUTIONS_PRIVATE_PYPI_PAT

# TODO: get poetry version from pyproject file?
RUN pip install --upgrade pip && \
    pip install poetry==1.7.1
RUN poetry config http-basic.solutions-private-pypi PAT ${SOLUTIONS_PRIVATE_PYPI_PAT}

COPY pyproject.toml poetry.lock /app/
COPY src/ /app/src/
COPY README.rst /app/

WORKDIR /app

# TODO: include documentation in the package?

RUN poetry install --only build -vv && \
    poetry build --format wheel && \
    poetry export --without-hashes --format requirements.txt --output requirements_api.txt
{% if cookiecutter.with_dash_ui == "yes" %}
RUN poetry export --only ui --without-hashes --format requirements.txt --output requirements_ui.txt
{% endif %}

# === API Stage ===
FROM python:3.10-alpine as solution_api

# credentials will only be available during image built
ARG SOLUTIONS_PRIVATE_PYPI_PAT

COPY --from=base /app/dist/*.whl /dist/
COPY --from=base /app/requirements_api.txt /dist/

# required by psutil for the psutil._psutil_linux extension
# TODO: how can we skip it and use a pre-built psutil that already includes it?
RUN apk add --no-cache build-base linux-headers

RUN pip install --upgrade pip && \
    pip install /dist/*.whl -r /dist/requirements_api.txt --extra-index-url "https://PAT:${SOLUTIONS_PRIVATE_PYPI_PAT}@pkgs.dev.azure.com/pyansys/_packaging/ansys-solutions/pypi/simple/"
RUN apk del build-base linux-headers && \
    rm -rf /var/cache/apk/* /root/.cache/pip/* /dist

# Launch API server directly with uvicorn
ENTRYPOINT ["uvicorn", "ansys.saf.glow.api:app"]

{% if cookiecutter.with_dash_ui == "yes" %}
# === UI Stage ===
# Currently, UI is designed as an extra of the API server, that's why it's built over the API image, including its dependencies.
FROM solution_api as solution_ui

COPY --from=base /app/requirements_ui.txt /dist/

RUN pip install -r /dist/requirements_ui.txt --extra-index-url "https://PAT:${SOLUTIONS_PRIVATE_PYPI_PAT}@pkgs.dev.azure.com/pyansys/_packaging/ansys-solutions/pypi/simple/"
RUN rm -rf /root/.cache/pip/* /dist

# Exposing UI app to be directly called with uvicorn is not available yet. Fallback to glow_engine CLI.
ENTRYPOINT ["glow_engine", "ui"]
{% endif %}
