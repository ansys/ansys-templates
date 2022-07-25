## Containerized deployment

### Usage

#### Build

```sh
$ docker build \
    -f docker/Dockerfile \
    -t $USER/{{cookiecutter.__project_name_slug}} \
    .
```

```ps1
> docker build `
    -f docker/Dockerfile `
    -t $env:UserName/{{cookiecutter.__project_name_slug}} `
    .
```

#### Run

```sh
$ docker run \
    -it \
    --rm \
    $USER/{{cookiecutter.__project_name_slug}}
```

```ps1
> docker run `
    -it `
    --rm `
    $env:UserName/{{cookiecutter.__project_name_slug}}
```

#### Diagnose

```sh
$ docker run \
    -it \
    --rm \
    --entrypoint=bash \
    $USER/{{cookiecutter.__project_name_slug}}
```

```ps1
> docker run `
    -it `
    --rm `
    --entrypoint=bash `
    $env:UserName/{{cookiecutter.__project_name_slug}}
```

#### Compose

```sh
$ docker-compose \
    -f docker/compose.yaml \
    up \
    --build
```

```ps1
> docker-compose `
    -f docker/compose.yaml `
    up `
    --build
```
