FROM python:{{ cookiecutter.requires_python }} AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y

RUN mkdir /app
RUN mkdir /src

COPY ../src/ /app/src/
COPY requirements/requirements_build.txt /app/src/

WORKDIR /app/src

RUN python -m pip install --no-cache-dir --upgrade pip
RUN python -m pip install --no-cache-dir -r requirements_build.txt

FROM base AS test

COPY requirements/requirements_tests.txt ./

RUN pip install --no-cache-dir -r requirements_tests.txt

COPY /tests ../tests/

WORKDIR /app

RUN pytest tests


FROM base AS final

LABEL org.opencontainers.image.authors=ericsson

EXPOSE 5000

ENTRYPOINT [ "python", "server.py" ]