## Containerized deployment

### Usage

#### Build

```sh
$ docker build \
    -f docker/Dockerfile \
    -t $USER/project \
    .
```

```ps1
> docker build `
    -f docker/Dockerfile `
    -t $env:UserName/project `
    .
```

#### Run

```sh
$ docker run \
    -it \
    --rm \
    $USER/project
```

```ps1
> docker run `
    -it `
    --rm `
    $env:UserName/project
```

#### Diagnose

```sh
$ docker run \
    -it \
    --rm \
    --entrypoint=bash \
    $USER/project
```

```ps1
> docker run `
    -it `
    --rm `
    --entrypoint=bash `
    $env:UserName/project
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
