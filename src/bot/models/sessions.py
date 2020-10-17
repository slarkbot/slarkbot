from sqlalchemy.orm import sessionmaker
from . import create_engine

engine = None

def create_session():

    if not engine:
        engine = create_engine()

    session = sessionmaker()
    session.configure(bind=engine)
    return session()
