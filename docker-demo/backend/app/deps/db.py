from app.db.session import SessionMaker


class DBConnection:
    def __init__(self):
        self.db = SessionMaker()

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc_value, traceback):
        self.db.close()


async def get_db():
    with DBConnection() as db:
        yield db


# def get_db():
#     """
#     Get the database session.
#     :return:
#     """
#     try:
#         db = SessionMaker()
#         yield db
#     finally:
#         db.close()
