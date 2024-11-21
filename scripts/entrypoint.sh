#!/usr/bin/env bash

# Saves the environment variables for the cronjobs (see cronrun.sh)
printenv > /environment-variables

# Start Cron
cron
tail -f /var/log/cron.log &

# Start Chroma
chroma run --path "$DATA_DIR" --host "0.0.0.0" --port "$CHROMA_PORT" --log-path "/var/log/chroma.log" &
CHROMA_PID=$!

# Start API
python3 -m t4search api &
API_PID=$!

# Start a Sync
python3 -m t4search sync &

# Wait and quit
wait -n $CHROMA_PID $API_PID
exit $?
