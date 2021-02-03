#!/usr/bin/env bash

function start_db () {
    docker container stop tuum-mongo || true && docker container rm -f tuum-mongo || true
    docker container stop vouch-redis || true && docker container rm -f vouch-redis || true
    docker run -d --name tuum-mongo                     \
        -v ${HOME}/.tuum-mongodb-data:/data/db          \
        -e MONGO_INITDB_ROOT_USERNAME=mongoadmin        \
        -e MONGO_INITDB_ROOT_PASSWORD=mongopass         \
        -p 27017:27017                                  \
        mongo
    docker run -d --name vouch-redis                       \
        -p 6379:6379                                      \
        redis
}

function docker_start () {
    start_db

    echo "Running using docker..."
    docker container stop vouch-restapi-node || true && docker container rm -f vouch-restapi-node || true
    docker build -t tuumtech/vouch-restapi-node .
    docker run --name vouch-restapi-node           \
      -v ${PWD}/.env:/src/.env                     \
      -p 8080:5000                                 \
      tuumtech/vouch-restapi-node
}

function start () {
    start_db

    virtualenv -p `which python3.7` .venv
    source .venv/bin/activate
    pip install --upgrade pip

    case `uname` in
    Linux )
        pip install -r requirements.txt
        ;;
    Darwin )
        pip install --global-option=build_ext \
                    --global-option="-I/usr/local/include" --global-option="-L/usr/local/lib" \
                    --global-option="-I/usr/local/opt/zlib/include" --global-option="-L/usr/local/opt/zlib/lib" -r requirements.txt
        ;;
    *)
    exit 1
    ;;
    esac

    gunicorn -b 0.0.0.0:8080 --reload app:application
}

function stop () {
    docker container stop tuum-mongo || true && docker container rm -f tuum-mongo || true
    docker container stop vouch-redis || true && docker container rm -f vouch-redis || true
    docker container stop vouch-restapi-node || true && docker container rm -f vouch-restapi-node || true
    ps -ef | grep gunicorn | awk '{print $2}' | xargs kill -9
}

case "$1" in
    start)
        start
        ;;
    docker)
        docker_start
        ;;
    stop)
        stop
        ;;
    *)
    echo "Usage: run.sh {start|docker|stop}"
    exit 1
esac