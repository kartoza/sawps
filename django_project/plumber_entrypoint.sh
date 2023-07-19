#!/bin/sh

# Exit script in case of error
set -e

echo $"\n\n\n"
echo "-----------------------------------------------------"
echo "STARTING PLUMBER ENTRYPOINT $(date)"
echo "-----------------------------------------------------"

# if [ ! -f /home/web/plumber_data/plumber.R ]
# then
# 	echo "Initial file not found, creating from template..."
#     cp /home/web/init_plumber.R /home/web/plumber_data/plumber.R
# fi

# start worker for Plumber
celery -A core worker -c 1 -Q plumber -l INFO -n plumberworker
