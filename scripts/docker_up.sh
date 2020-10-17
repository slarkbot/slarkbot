#!/bin/bash

cd scripts
source ../.env


docker run --rm --name $POSTGRES_DB \
    -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
    -e POSTGRES_USER=$POSTGRES_USER \
    -p $DATABASE_PORT:5432 \
    -v $HOME/docker/volumes/postgres:/var/lib/postgresql/data \
    -d \
    postgres