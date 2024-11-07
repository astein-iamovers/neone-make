# NEONE Server Setup

Welcome to the NEONE Server Setup, in this document you will find all the instructions to run a NE:ONE server and how to setup pub/sub in ONE Record

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed
- [Docker Compose](https://docs.docker.com/compose/install/) installed (make sure you have compose V2)
- [Git](https://git-scm.com/downloads) installed

## Step by step guide

1) Clone the repository
   ```bash
   git clone https://github.com/astein-iamovers/neone.git
   ```
2) Switch to the directory neone
   ```bash
   cd neone
   ```
   If you have Mac or Linux, please reset folder permissions 
   ```bash
   chmod -R 755 ./
   ```
4) Modify your .env file adding your variables

5) Start all services with [docker compose](https://docs.docker.com/compose/)
   ```bash
   docker compose up -d
   ```
6) Wait until all containers are up and running:
   ```bash
   [+] Running 6/6
    ✔ Network docker-compose_default            Created
    ✔ Container docker-compose-graph-db-1       Healthy
    ✔ Container neone-notification-forwarder-1  Started
    ✔ Container docker-compose-graph-db-setup-1 Started
    ✔ Container docker-compose-ne-one-server-1  Healty
    ✔ Container neone-ne-one-play-1             Started
    ✔ Container neone-ne-one-view-1             Started
        
    
   ```
7) Try to access the ONE Record Server by http://{baseUrl}:8080 using your favorite browser (replace baseUrl with your ONE Record URL). 
   You should see a HTTP Error 401, because you did not authenticate yet. But this confirms that the ONE Record Server is up and running.

# Overview of services

| Name | Description | Base URL / Admin UI |
|-|-|-|
| ne-one-1 | [ne-one server](https://git.openlogisticsfoundation.org/wg-digitalaircargo/ne-one) | http://{baseUrl}:8080 |
| ne-one view | [ne-one view](https://git.openlogisticsfoundation.org/wg-digitalaircargo/ne-one-view) | http://{baseUrl}:3000 |
| ne-one play | [ne-one play](https://github.com/aloccid-iata/neoneplay) | http://{baseUrl}:3001 |
| graphdb | GraphDB database as database backend for ne-one-1 repository neone | http://{baseUrl}:7200 |
| notification-forwarder | A Flask app (python) that processes incoming notifications | http://{baseUrl}:5000 |

## Postman Collection

We have prepared a Postman collection to test the ONE Record API. You will need to install Postman or a compatible software in order to use it.

1. [Download the Postman Collection here.](./assets/postman/Subscription.postman_collection.json) It will open a new github page, use the download button to get the file

2. [Download the Postman Environment here](./assets/postman/SubscriptionEnvironment.postman_environment.json). It will open a new github page, use the download button to get the file

3. Import the Environment in Postman and Update the Variables

4. Import the Collection in Postman

5. In the Environments tab, select the IAM Test environment. 

6. Select Collections on the right menu and open the IAM Test collection already imported

7. Use the Token Request call to generate and access token

8. Copy the access token (it might be a long string, please copy the full content) in the Authorization tab of the collection folder (Subscription). Now all API calls will in the folder will use the same bearer token. Alternatively you can copy the token to the Authorization tab of each API call.

10. Run the call named "Subscription S1 to S2 Product" to have the ne-one-1 server subscribing to all Product logistics object created on ne-one-2

11. Approve the subscription on ne-one-2 with the call "Approve subscription"

12. Generate a new Product on ne-one-2 using the call "Create Product". Looking at the log of ne-one-1 you should receive a notification.

IMPORTANT: In the current setup, *ne-one-1* will receive a notification and send a ping to the mock server. To modify this behavior, update the 'QUARKUS_REST_CLIENT_NOTIFICATION_CLIENT_URL' property in the *ne-one-1* configuration within the Docker Compose file to point to your server. *Ne-one-1* will then forward the notification to *(your-host)/notifications*.

## Add NE:ONE server into NE:ONE Play

1. Connect to NE:ONE Play http://{baseUrl}:3001 

2. Click on the setting button in the top-right corner (cog icon)

3. Add your ne-one-1 server following this instruction:

    - Organization Name: <Choose a name (any string is accepted)>
    - Protocol: http
    - Host: http://{baseUrl}:8080  
    - Token : <Use the postman collection to generate a token and copy it here (follow the previous paragraph)>
    - Color : pick up a random color

4. Now you can start using NE:ONE Play. 

