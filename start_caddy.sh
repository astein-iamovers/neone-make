#!/bin/bash

# Load environment variables
source .env

# Separate base URL and path
BASE_URL=$(echo "$MAKE_WEBHOOK_URL" | sed -E 's|^((https?://[^/]+)).*|\1|')
PATH_ONLY=$(echo "$MAKE_WEBHOOK_URL" | sed -E 's|^https?://[^/]+(/.*)|\1|')

# Replace placeholders in Caddyfile.template and save as Caddyfile
sed -e "s|{MAKE_WEBHOOK_HOST}|$MAKE_WEBHOOK_HOST|g" \
    -e "s|{MAKE_WEBHOOK_PATH}|$MAKE_WEBHOOK_PATH|g" \
    Caddyfile.template > Caddyfile

# Start Caddy with the generated Caddyfile
caddy run --config Caddyfile
