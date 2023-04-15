# ---------------------------
FROM python:{{ cookiecutter.requires_python }}-slim AS base

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

COPY requirements/requirements_build.txt ./

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements_build.txt

WORKDIR /app

# ---------------------------
FROM base AS test

COPY requirements/requirements_test.txt ./

RUN pip install --no-cache-dir -r requirements_test.txt

COPY . .

RUN pytest tests

# ---------------------------
FROM base AS final
LABEL org.opencontainers.image.authors={{ cookiecutter.__project_name_slug }}

COPY src .

ENTRYPOINT [ "python", "main.py" ]