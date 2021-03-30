#!/bin/bash

cd ./scripts
source ../.env

psql -U $POSTGRES_USER \
    -h localhost \
    -p $DATABASE_PORT \
    -v db_name=$POSTGRES_DB \
    -d $POSTGRES_DB \
    -f create_database.sql -W
