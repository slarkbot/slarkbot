import os

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()


def create_database_engine():
    db_user = os.getenv("POSTGRES_USER")
    db_password = os.getenv("POSTGRES_PASSWORD")
    db_port = os.getenv("DATABASE_PORT")
    db_name = os.getenv("POSTGRES_DB")

    connection_string = (
        f"postgresql://{db_user}:{db_password}@localhost:{db_port}/{db_name}"
    )
    print(connection_string)
    database_engine = create_engine(connection_string)
    return database_engine
