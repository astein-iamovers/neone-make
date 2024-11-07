#!/bin/bash

# Check if the repository already exists
REPO_STATUS=$(curl -o /dev/null -s -w "%{http_code}" -X GET http://graph-db:7200/rest/repositories/"$NEONE_REPO_ID")

if [ "$REPO_STATUS" -eq 404 ]; then
    echo "Creating repository '$NEONE_REPO_ID'..."
    curl -X POST --header 'Content-Type: multipart/form-data' \
         -F "config=@/opt/neone/graphdb/neone-repository.ttl" \
         http://graph-db:7200/rest/repositories
    echo "Repository '$NEONE_REPO_ID' created."

    # Set the new repository as active
    curl -X PUT --header 'Content-Type: text/plain' \
         --data "$NEONE_REPO_ID" \
         http://graph-db:7200/rest/activeRepository
    echo "Repository '$NEONE_REPO_ID' set as active."
elif [ "$REPO_STATUS" -eq 200 ]; then
    echo "Repository '$NEONE_REPO_ID' already exists."
else
    echo "Error checking repository status - Server returned $REPO_STATUS"
    exit 1
fi
