# ---------------------------
FROM python:{{ cookiecutter.requires_python }}-slim AS base

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y

COPY requirements/requirements.txt ./

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

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

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
# TODO Disable to be able to write to /var/log/
# RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
# USER appuser

ENTRYPOINT [ "python", "main.py" ]