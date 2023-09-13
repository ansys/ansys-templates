# ---------------------------
FROM python:3.7-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements/requirements_build.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements_build.txt

# ---------------------------
FROM base AS test

COPY requirements/requirements_tests.txt .

RUN pip install --no-cache-dir -r requirements_test.txt

COPY . .

RUN pytest tests

# ---------------------------
FROM base AS final
LABEL org.opencontainers.image.authors=project

EXPOSE 80

COPY src .

ENTRYPOINT [ "uvicorn", "server:app", "--host", "0.0.0.0", "--port", "80" ]