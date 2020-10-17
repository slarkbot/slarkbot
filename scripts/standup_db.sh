#!/bin/bash

cd ./scripts
source ../.env

dropdb dota_stats
psql -U $POSTGRES_USER \
    -p $DATABASE_PORT \
    -v db_name=$POSTGRES_DB \
    -f create_database.sql