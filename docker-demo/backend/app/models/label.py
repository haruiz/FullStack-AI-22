from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime

from app.db.orm_base import OrmBaseModel
from sqlalchemy import event
from sqlalchemy import DDL

"""
ORM class to interact with the image_records table in the database
"""


class Label(OrmBaseModel):
    label_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    label = Column(String(100), nullable=False, unique=True)
    description = Column(String(1000), nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow)


restart_seq = DDL("ALTER SEQUENCE %(table)s_label_id_seq RESTART WITH 100;")

event.listen(
    Label.__table__, "after_create", restart_seq.execute_if(dialect="postgresql")
)
