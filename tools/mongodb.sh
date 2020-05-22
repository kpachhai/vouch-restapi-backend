#!/bin/bash

docker container stop vouch-mongo || true && docker container rm -f vouch-mongo || true

# start a mongodb docker container
docker run -d --name vouch-mongo                        \
    -v "$PWD/.mongodb-data:/data/db"            \
    -e MONGODB_USERNAME=mongoadmin                      \
    -e MONGODB_PASSWORD=vouchmongo                      \
    -e MONGODB_DATABASE=vouchdb                         \
    -p 27018:27017                                      \
    mongo
