from sqlalchemy.orm import sessionmaker


def create_session(engine):
    session = sessionmaker()
    session.configure(engine)
    return session
