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


# Create a singleton instance of the ImageRecordCRUD class
image_record = ImageRecordCRUD()
