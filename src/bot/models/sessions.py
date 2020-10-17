from sqlalchemy.orm import sessionmaker
from . import create_database_engine

engine = None

def create_session():

    # TODO: this is a hack, want engine singleton but its python ..
    try:
        if not engine:
            engine = create_database_engine()
    except UnboundLocalError:
        engine = create_database_engine()


    session = sessionmaker()
    session.configure(bind=engine)
    return session()
