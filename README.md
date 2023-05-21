# back

## Docker

#### Build container

```$ docker-compose build```

#### Start services

```$ docker-compose up```

#### List images

```$ docker images```

## Dependencies

(Always execute this before installing and after any change in *pyproject.toml* file)

```$ poetry lock```

#### Install Poetry [DEV]

```$ poetry install -E dev```

#### Install Poetry [MAIN]

```$ poetry install```

## Tests

#### Run tests

```$ poetry run pytest tests```
