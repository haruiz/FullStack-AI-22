from app.db.session import SessionMaker


def get_db():
    """
    Get the database session.
    :return:
    """
    try:
        db = SessionMaker()
        yield db
    finally:
        db.close()
