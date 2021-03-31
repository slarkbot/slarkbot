
cd ./scripts
source ../.env

PGPASSWORD=$POSTGRES_PASSWORD dropdb -p $DATABASE_PORT -h localhost $POSTGRES_DB
