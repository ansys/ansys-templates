## Containerized deployment

### Usage

```sh
# Build
$ docker build \
    -t $USER/{{cookiecutter.__project_name_slug}} \
    .
```

```sh
# Run
$ docker run \
    -it \
    $USER/{{cookiecutter.__project_name_slug}}
```

```sh
# Diagnose
$ docker run \
    -it \
    --entrypoint=bash \
    $USER/{{cookiecutter.__project_name_slug}}
```

```sh
# Deploy through docker-compose
$ docker-compose up --build
```
