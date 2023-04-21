#!/usr/bin/env bash
#
# IMPORTANT: Change this file only in directory Standalone!

if [ ! -z "$SE_OPTS" ]; then
  echo "Appending Webserver options: ${SE_OPTS}"
fi

/opt/bin/generate_config

echo "Starting Webserver..."
cd /app && ./selenium_webserver
