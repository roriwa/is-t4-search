ARG PYTHON_VERSION=3.10

FROM python:${PYTHON_VERSION}-slim AS base

FROM base AS builder

WORKDIR /code

# generates the requirements.txt from the Pipfile[.lock]
RUN pip install --root-user-action ignore --no-cache-dir --disable-pip-version-check -U pipenv
COPY Pipfile* ./
RUN pipenv requirements > requirements.txt

FROM base AS runtime

LABEL description="Information Systems - Team 4 - Search Index"
LABEL repository="https://github.com/roriwa/is-t4-search"

WORKDIR /code
VOLUME ["/data"]

RUN apt-get update && \
    apt-get install --no-install-recommends -y cron curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# add and install dependencies
COPY --from=builder /code/requirements.txt .
RUN pip install --root-user-action ignore --disable-pip-version-check --upgrade -r requirements.txt

# add the entrypoint which will be executed
COPY Dockerfile.assets/entrypoint.sh /entrypoint.sh
RUN chmod 0777 /entrypoint.sh

# default configuration.
COPY Dockerfile.assets/config.default.yaml /etc/t4search/config.yaml

# configures cron
COPY Dockerfile.assets/cronjob /etc/cron.d/cronjob
RUN chmod 0644 /etc/cron.d/cronjob
RUN crontab /etc/cron.d/cronjob
RUN touch /var/log/cron.log
COPY Dockerfile.assets/cronrun.sh /cronrun.sh
RUN chmod 0777 /cronrun.sh

# copy or python-module
COPY src/ /opt/src/

# adds our module to the path to allow execution via `python3 -m`
ENV PYTHONPATH "$PYTHONPATH:/opt/src"
# Enable UTF-8 mode for operating system interfaces
ENV PYTHONUTF8 1
# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE 1
# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED 1

# ----- congfiguration options -----

# permanent data storage
ENV DATA_DIR "/data"
# the port where chroma should run on
ENV CHROMA_PORT 9010
# where the configuration file is located
ENV CONFIG_FILE "/config.yaml"

# ----------------------------------

# where our api-server will run on
EXPOSE 80

ENTRYPOINT ["/entrypoint.sh"]
