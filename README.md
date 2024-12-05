# is-t4-search
Information Systems - Team 4 - Search Index

<!-- TOC -->
* [is-t4-search](#is-t4-search)
  * [usage](#usage)
  * [configuration](#configuration)
  * [developers](#developers)
    * [starting (normal)](#starting-normal)
    * [starting (with reload)](#starting-with-reload)
<!-- TOC -->

## usage

`docker-compose.yaml`
```yaml
services:
  t4search:
    image: ghcr.io/roriwa/t4search:latest
    ports:
      - "8080:80"
    volumes:
      - ./data:/data
      - ./config.yaml:/config.yaml
```

don't forget to create the `config.yaml`

## configuration

```yaml
api:
  host: "0.0.0.0"
  port: 8000
chroma:
  host: "0.0.0.0"
  port: 9010
logging:
  level: # DEBUG | INFO | WARNING | ERROR | CRITICAL
  format: # "@SHORT" | "@LONG" | "CUSTOM"
```

## developers

```shell
# initial setup
pip3 install -U pipenv
PIPENV_VENV_IN_PROJECT=1 pipenv install --dev
```

when starting, don't forget to have a chroma server running

```shell
chomra run --port 8000 --path ./chroma_data --log-path ./chroma.log
```

### starting (normal)

```shell
./run.sh api
./run.sh sync
```

### starting (with reload)

```shell
fastapi dev src/t4search/api
```
