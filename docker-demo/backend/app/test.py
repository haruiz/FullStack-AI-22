from app.db import create_db, drop_db
import app.crud as crud
from app.deps import DBConnection


if __name__ == "__main__":
    create_db()
    with DBConnection() as db:
        print(crud.image_record.fetch_all(db=db))
