from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime

from app.db.orm_base import OrmBaseModel

"""
ORM class to interact with the image_records table in the database
"""


class ImageRecord(OrmBaseModel):
    image_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    filename = Column(String(50), nullable=False)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    size = Column(Integer, nullable=False)
    size_str = Column(String(10), nullable=False)
    fmt = Column(String(10), nullable=False)
    mode = Column(String(10), nullable=False)
    label = Column(String(100), nullable=False)
    notes = Column(String(1000), nullable=True)
    lat = Column(Float, nullable=True)
    lng = Column(Float, nullable=True)
    bucket = Column(String(100), nullable=True)
    blob_name = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow)
