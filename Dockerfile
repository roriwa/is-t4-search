FROM python:3.10-slim AS base

FROM base AS builder

WORKDIR /code

RUN pip install --root-user-action ignore --no-cache-dir --disable-pip-version-check -U pipenv
COPY Pipfile* ./
RUN pipenv requirements > requirements.txt

FROM base AS runtime

RUN apt-get update && apt-get install -y cron

LABEL description="Information Systems - Team 4 - Search Index"
LABEL repository="https://github.com/roriwa/is-t4-search"

WORKDIR /code
VOLUME ["/data"]

COPY --from=builder /code/requirements.txt .
RUN pip install --root-user-action ignore --no-cache-dir --disable-pip-version-check --upgrade -r requirements.txt

COPY scripts/entrypoint.sh /entrypoint.sh
RUN chmod 0777 /entrypoint.sh

COPY scripts/config.default.yaml /config.yaml

COPY scripts/cronjob /etc/cron.d/cronjob
RUN chmod 0644 /etc/cron.d/cronjob
COPY scripts/cronrun.sh /cronrun.sh
RUN chmod 0777 /cronrun.sh
RUN crontab /etc/cron.d/cronjob
RUN touch /var/log/cron.log

COPY src/ /opt/src/

ENV PYTHONPATH "$PYTHONPATH:/opt/src"
ENV PYTHONUTF8 1

ENV DATA_DIR "/data"
ENV CHROMA_PORT 9010
ENV CONFIG_FILE "/config.yaml"

EXPOSE 80

ENTRYPOINT ["/entrypoint.sh"]
