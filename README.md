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

Go into the directory of your choice. (e.g. `/srv/t4search`).
Then create the following files.

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

`.env`
```bash
T4SEARCH_MONGO_URI=#TODO
```

`config.yaml`
```yaml
# yes. empty if you don't want to change anything
```

And finally start it with
```bash
docker compose up -d
```

The API should be available under port 8080.
Inspect the API-Documentation via `http://localhost:8080/redoc`

## configuration

example!!

```yaml
api:
  # which host to bind to
  host: "0.0.0.0"
  # which port to bind to
  port: 8000
chroma:
  # on which host the chroma-db runs
  host: "0.0.0.0"
  # on which port the chroma-db runs
  port: 9010
sync:
  # whether to also save the content of documents instead of just their embeddings
  # warning: increases disk usage
  save_documents: false
logging:
  # logging details
  level: # DEBUG | INFO | WARNING | ERROR | CRITICAL
  # logging format
  format: # "@SHORT" | "@LONG" | "CUSTOM"
```

## developers

```shell
# initial setup
pip3 install -U pipenv
PIPENV_VENV_IN_PROJECT=1 pipenv install --dev
./run reset
./run init
```

when starting, don't forget to have a chroma server running

```shell
chroma run --port 9010 --path ./chroma_data --log-path ./chroma.log
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
