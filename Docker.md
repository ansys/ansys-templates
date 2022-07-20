## Containerized deployment

### Usage

#### Build

```sh
$ docker build \
    -t $USER/project \
    .
```

```ps1
> docker build `
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
$ docker-compose up --build
```

```ps1
> docker-compose up --build
```
