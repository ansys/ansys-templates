# ---------------------------
FROM python:{{ cookiecutter.requires_python }}-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements/requirements_build.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements_build.txt

RUN mkdir stubs

ADD protobufs/ ./protobufs/
RUN python -m grpc_tools.protoc  \
    -I ./protobufs  \
    --python_out=./stubs \
    --grpc_python_out=./stubs  \
    ./protobufs/*.proto

# ---------------------------
FROM base AS test

COPY requirements/requirements_tests.txt .

RUN pip install --no-cache-dir -r requirements_test.txt

COPY . .

RUN pytest tests

# ---------------------------
FROM base AS final
LABEL org.opencontainers.image.authors={{ cookiecutter.__project_name_slug }}

EXPOSE 50051

COPY src .

ENTRYPOINT [ "python", "server.py" ]