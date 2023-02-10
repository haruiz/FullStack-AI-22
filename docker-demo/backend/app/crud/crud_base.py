from typing import Any, Generic, List, Optional, Type, TypeVar, Tuple

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.orm_base import OrmBaseModel

ModelType = TypeVar("ModelType", bound=OrmBaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

"""
Base CRUD Model for SQLAlchemy ORM
"""


class CrudBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model_cls: Type[ModelType]):  # 2
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model_cls = model_cls

    def get(self, db: Session, model_id: Any) -> Optional[ModelType]:
        """
        Get a record by its id.
        :param db:
        :param model_id:
        :return:
        """
        return db.get(self.model_cls, model_id)

    def fetch_all(self, db: Session) -> list[tuple[Any]]:
        """
        Read all records.
        :param db:
        :return:
        """
        return db.query(self.model_cls).all()

    def create(self, db: Session, *, entity: CreateSchemaType) -> ModelType:
        """
        Create a new record.
        :param db:
        :param entity:
        :return:
        """
        obj_in_data = jsonable_encoder(entity)
        db_obj = self.model_cls(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create_batch(self, db: Session, entities: List[CreateSchemaType]):
        """
        Create a list of records.
        :param db:
        :param entities:
        :return:
        """
        db_objs = list(
            map(lambda entity: self.model_cls(**jsonable_encoder(entity)), entities)
        )
        db.add_all(db_objs)
        db.commit()

    def update(
        self, db: Session, *, model_id: Any, entity: UpdateSchemaType
    ) -> ModelType:
        """
        Update a record.
        :param db:
        :param model_id:
        :param entity:
        :return:
        """
        db_obj = self.get(db, model_id)
        if db_obj is None:
            raise Exception("Object not found")
        obj_in_data = jsonable_encoder(entity)
        for key, value in obj_in_data.items():
            setattr(db_obj, key, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
