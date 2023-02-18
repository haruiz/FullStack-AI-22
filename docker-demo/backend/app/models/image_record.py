from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from app.db.orm_base import OrmBaseModel
from sqlalchemy import event
from sqlalchemy import DDL

"""
ORM class to interact with the image_records table in the database
"""


class ImageRecord(OrmBaseModel):
    image_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    filename = Column(String(50), nullable=False, unique=True)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    size = Column(Integer, nullable=False)
    size_str = Column(String(10), nullable=False)
    fmt = Column(String(10), nullable=False)
    mode = Column(String(10), nullable=False)
    notes = Column(String(1000), nullable=True)
    lat = Column(Float, nullable=True)
    lng = Column(Float, nullable=True)
    bucket = Column(String(100), nullable=True)
    blob_name = Column(String(100), nullable=True)
    label_id = Column(Integer, ForeignKey("label.label_id"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow)


restart_seq = DDL("ALTER SEQUENCE %(table)s_image_id_seq RESTART WITH 100;")

event.listen(
    ImageRecord.__table__, "after_create", restart_seq.execute_if(dialect="postgresql")
)
