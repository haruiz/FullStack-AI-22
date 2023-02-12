from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime

from app.db.orm_base import OrmBaseModel


class Label(OrmBaseModel):
    label_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    label = Column(String(100), nullable=False)
    description = Column(String(1000), nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow)
