#!/bin/bash

docker container stop vouch-mongo || true && docker container rm -f vouch-mongo || true

# start a mongodb docker container
docker run -d --name vouch-mongo                        \
    -e MONGO_INITDB_ROOT_USERNAME=mongoadmin                      \
    -e MONGO_INITDB_ROOT_PASSWORD=vouchmongo                      \
    -p 27018:27017                                      \
    mongo
