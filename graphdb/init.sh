#!/bin/bash

NEONE_REPO1_HTTP_STATUS=$(curl -o /dev/null -s -w '%{http_code}' -i http://graph-db:7200/rest/repositories/"$NEONE_REPO_ID")

#NEONE_REPO2_HTTP_STATUS=$(curl -o /dev/null -s -w '%{http_code}' -i http://graph-db:7200/rest/repositories/"$NEONE_REPO_ID_2")

if [ "$NEONE_REPO1_HTTP_STATUS" -eq 404 ]; then
    echo "Creating neone repository $NEONE_REPO_ID"
    curl --fail -X POST --header 'Content-Type:multipart/form-data' -F 'config=@/opt/neone/graphdb/neone-repository.ttl' 'http://graph-db:7200/rest/repositories'
elif [ "$NEONE_REPO1_HTTP_STATUS" -eq 200 ]; then
    echo "Repository already exists"
else
    echo "Error creating repository - Server returned $NEONE_REPO1_HTTP_STATUS for repo $NEONE_REPO_ID"
    exit 1
fi

# Uncomment and edit the following lines to create a second repository if needed

#if [ "$NEONE_REPO2_HTTP_STATUS" -eq 404 ]; then
#    echo "Creating neone repository $NEONE_REPO_ID_2"
#    curl --fail -X POST --header 'Content-Type:multipart/form-data' -F 'config=@/opt/neone/graphdb/neone-repository-2.ttl' 'http://graph-db:7200/rest/repositories'
#elif [ "$NEONE_REPO2_HTTP_STATUS" -eq 200 ]; then
#    echo "Repository already exists"
#else
#    echo "Error creating repository - Server returned $NEONE_REPO2_HTTP_STATUS for repo $NEONE_REPO_ID_2"
#    exit 1
#fi
