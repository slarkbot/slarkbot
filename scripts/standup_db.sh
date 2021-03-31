#!/bin/bash

cd ./scripts
source ../.env

PGPASSWORD=$POSTGRES_PASSWORD createdb -p $DATABASE_PORT -h localhost $POSTGRES_DB -w

PGPASSWORD=$POSTGRES_PASSWORD \
psql -U $POSTGRES_USER \
    -h localhost \
    -p $DATABASE_PORT \
    -v db_name=$POSTGRES_DB \
    -d $POSTGRES_DB \
    -f create_database.sql 
