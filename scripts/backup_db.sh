
source ./.env
cd ./scripts

echo "Creating pg_dump of $POSTGRES_DB"
pg_dump $POSTGRES_DB > $POSTGRES_DB.sql

echo "backup complete!"
