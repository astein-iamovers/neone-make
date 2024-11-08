#!/bin/bash

# Load environment variables
source .env

# Replace placeholders in Caddyfile.template and save as Caddyfile
sed -e "s|{MAKE_WEBHOOK_PATH}|$MAKE_WEBHOOK_PATH|g" \
    -e "s|{MAKE_WEBHOOK_SCHEME}|${MAKE_WEBHOOK_SCHEME:-https}|g" \
    -e "s|{MAKE_WEBHOOK_HOST}|$MAKE_WEBHOOK_HOST|g" \
    Caddyfile.template > Caddyfile

# Start Caddy with the generated Caddyfile
caddy run --config Caddyfile
