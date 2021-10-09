
cd ./scripts
source ../.env

PGPASSWORD=$POSTGRES_PASSWORD dropdb -p $DATABASE_PORT -U $POSTGRES_USER -h localhost $POSTGRES_DB
