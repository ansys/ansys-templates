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
    $USER/project
```

```ps1
> docker run `
    -it `
    $env:UserName/project
```

#### Diagnose

```sh
$ docker run \
    -it \
    --entrypoint=bash \
    $USER/project
```

```ps1
> docker run `
    -it `
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
