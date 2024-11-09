# NEONE Server Setup - Forward Notifications to a Make Webhook

Welcome to the NEONE Server Setup, in this document you will find the instructions to run a NE:ONE server.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed
- [Git](https://git-scm.com/downloads) installed

## Step by step guide

1) Clone this repository
   ```bash
   git clone https://github.com/astein-iamovers/neone-make.git
   ```
2) Switch to the directory neone
   ```bash
   cd neone-make
   ```
   If you have Mac or Linux, please reset folder permissions 
   ```bash
   chmod -R 755 ./
   ```
4) Modify your .env file with the nano editor.
   ```bash
   nano .env
   ```
   Paste your variables
   - HOST: the URL of your ONE Record Server
   - CLIENT_ID: given by IAM
   - CLIENT_SECRET: given by IAM
   - AUDIENCE: given by IAM

5) Modify the Caddyfile adding your Make webhook details
   ```bash
   nano Caddyfile
   ```
   Replace the placeholders MAKE_HOST and MAKE_PATH with your webhook details.
   Note that the URL needs to be split. If your webhook is https://hook.us2.make.com/zbugts03uc1i2ouvsx1ksnwzv07cql1x, then the MAKE_HOST is https://hook.us2.make.com and the MAKE_PATH is /zbugts03uc1i2ouvsx1ksnwzv07cql1x (include the initial hash)
   
   To save an exit: ctrl+x then Y then Enter
6) Start all services with [docker compose](https://docs.docker.com/compose/)
   ```bash
   docker compose up -d
   ```
7) Wait until all containers are up and running:
   ```bash
   [+] Running 6/6
    ✔ Network docker-compose_default            Created
    ✔ Container docker-compose-graph-db-1       Healthy
    ✔ Container docker-compose-graph-db-setup-1 Started
    ✔ Container docker-compose-ne-one-server-1  Healty
    ✔ Container neone-ne-one-play-1             Started
    ✔ Container neone-ne-one-view-1             Started
    ✔ Container caddy-1                         Started
        
    
   ```
8) Try to access the ONE Record Server by http://{baseUrl}:8080 using your favorite browser (replace baseUrl with your ONE Record URL). 
   You should see a HTTP Error 401, because you did not authenticate yet. But this confirms that the ONE Record Server is up and running.

# Overview of services

| Name | Description | Base URL / Admin UI |
|-|-|-|
| ne-one-server | [ne-one server](https://git.openlogisticsfoundation.org/wg-digitalaircargo/ne-one) | http://{baseUrl}:8080 |
| ne-one-view | [ne-one view](https://git.openlogisticsfoundation.org/wg-digitalaircargo/ne-one-view) | http://{baseUrl}:3000 |
| ne-one-play | [ne-one play](https://github.com/aloccid-iata/neoneplay) | http://{baseUrl}:3001 |
| graphdb | GraphDB database as database backend for ne-one-1 repository neone | http://{baseUrl}:7200 |

