#!/bin/bash

source .env

docker build -t eg_dotabot .

docker run --rm \
    --name ${POSTGRES_DB}_database \
    -p $DATABASE_PORT:3432 \
    -d eg_dotabot

# docker run --rm --name $POSTGRES_DB \
#     -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
#     -e POSTGRES_USER=$POSTGRES_USER \
#     -p $DATABASE_PORT:5432 \
#     -v $HOME/docker/volumes/postgres:/var/lib/postgresql/data \
#     -d \
#     postgres