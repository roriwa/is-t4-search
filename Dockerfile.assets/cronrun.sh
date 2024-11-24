#!/usr/bin/env bash
# wrapper script to run environment variables for a cron job

set -a
. /environment-variables
set +a

/usr/bin/env "$@"
