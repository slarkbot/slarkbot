cd ./scripts
source ../.env

PGPASSWORD=$POSTGRES_PASSWORD \
psql -U $POSTGRES_USER \
    -h localhost \
    -p $DATABASE_PORT \
    -v db_name=$POSTGRES_DB \
    -d $POSTGRES_DB \
    -f rebuild_constants.sql 

cd ..
python ./scripts/seed.py