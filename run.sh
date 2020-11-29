#!/usr/bin/env bash

function start () {
    docker container stop vouch-mongo || true && docker container rm -f vouch-mongo || true
    docker container stop vouch-redis || true && docker container rm -f vouch-redis || true
    docker run -d --name vouch-mongo                     \
        -v ${PWD}/.mongodb-data:/data/db                         \
        -e MONGO_INITDB_ROOT_USERNAME=mongoadmin          \
        -e MONGO_INITDB_ROOT_PASSWORD=vouchmongo         \
        -p 27018:27017                                    \
        mongo
    docker run -d --name vouch-redis                       \
        -p 6379:6379                                      \
        redis

    virtualenv -p `which python3.7` .venv
    source .venv/bin/activate
    pip install --upgrade pip

    case `uname` in
    Linux )
        pip install -r requirements.txt
        ;;
    Darwin )
        pip install --global-option=build_ext --global-option="-I/usr/local/include" --global-option="-L/usr/local/lib" -r requirements.txt
        ;;
    *)
    exit 1
    ;;
    esac

    gunicorn -b 0.0.0.0:8080 --reload app:application
}

function stop () {
    docker container stop vouch-mongo || true && docker container rm -f vouch-mongo || true
    ps -ef | grep gunicorn | awk '{print $2}' | xargs kill -9
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    *)
    echo "Usage: run.sh {start|stop}"
    exit 1
esac