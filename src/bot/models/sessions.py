from sqlalchemy.orm import sessionmaker
from . import create_database_engine

engine = None


def create_session():

    if not engine:
        engine = create_database_engine()

    session = sessionmaker()
    session.configure(bind=engine)
    return session()
