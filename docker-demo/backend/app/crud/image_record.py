from typing import List

from sqlalchemy.orm import Session

from app.crud.crud_base import CrudBase
import app.models as models
import app.schemas as schemas
from app.utils import Singleton

"""
This class is a CRUD class for the predictions table.
"""


class ImageRecordCRUD(
    CrudBase[schemas.ImageRecord, schemas.ImageRecordCreate, schemas.ImageRecordUpdate],
    metaclass=Singleton,
):
    def __init__(self):
        super().__init__(models.ImageRecord)

    def check_if_exists(self, db: Session, filename: str) -> bool:
        """
        Check if an image record exists in the database
        :param db:
        :param filename:
        :return:
        """
        db_obj = (
            db.query(self.model_cls)
            .filter(self.model_cls.filename == filename)
            .first()
        )
        is_exist = db_obj is not None
        return is_exist


# Create a singleton instance of the ImageRecordCRUD class
image_record = ImageRecordCRUD()
