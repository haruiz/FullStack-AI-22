from sqlalchemy import create_engine, event
from sqlalchemy.orm import (
    sessionmaker,
)  # create a session factory to connect to the database
from decouple import config
from functools import wraps

from .orm_base import OrmBaseModel

SQLALCHEMY_DATABASE_URL = config("DATABASE_URL")
print(f"SQLALCHEMY_DATABASE_URL: {SQLALCHEMY_DATABASE_URL}")
engine = create_engine(SQLALCHEMY_DATABASE_URL)


def on_connect(dbapi_con, con_record):
    print(f"connection established to database {dbapi_con}")


event.listen(engine, "connect", on_connect)

# connect factory to the database
SessionMaker = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, expire_on_commit=False
)


def create_session(func):
    """
    Create a database session
    :param func:
    :return:
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        session = SessionMaker()
        try:
            result = func(*args, session=session, **kwargs)
            session.commit()
            return result
        except:
            session.rollback()
            raise
        finally:
            session.close()

    return wrapper


def create_db():
    """
    Create all tables in the database
    :return:
    """
    OrmBaseModel.metadata.create_all(bind=engine)


def drop_db():
    """
    Drop all tables in the database
    :return:
    """
    OrmBaseModel.metadata.drop_all(bind=engine)
