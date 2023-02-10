from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ImageRecordSchema(BaseModel):
    filename: str
    size: int
    size_str: str
    fmt: str
    width: int
    height: int
    mode: str
    label: str
    bucket: Optional[str]
    blob_name: Optional[str]
    notes: Optional[str]
    lat: Optional[float]
    lng: Optional[float]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class ImageRecordCreate(ImageRecordSchema):
    pass


class ImageRecordUpdate(ImageRecordSchema):
    pass


class ImageRecord(ImageRecordSchema):
    image_id: int = None

    class Config:
        orm_mode = True
