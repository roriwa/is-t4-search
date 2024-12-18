#!/usr/bin/env bash
set -e

cd "$DATA_DIR"

# Saves the environment variables for the cronjobs (see cronrun.sh)
printenv > /environment-variables

# Start Cron
cron
tail -f /var/log/cron.log &

# Start Chroma
chroma run --path "./chroma" --host "0.0.0.0" --port "$CHROMA_PORT" --log-path "/var/log/chroma.log" &
CHROMA_PID=$!

while ! curl -s -o /dev/null "http://0.0.0.0:$CHROMA_PORT/api/v1/heartbeat"; do
  echo "Waiting for chroma to start..."
  sleep 1s
done

# Start API
python3 -m t4search api &
API_PID=$!

# Start a Sync
python3 -m t4search sync &

# Wait and quit
wait -n $CHROMA_PID $API_PID
exit $?
