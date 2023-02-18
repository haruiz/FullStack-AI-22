from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class LabelSchema(BaseModel):
    label: str
    description: Optional[str] = None
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class LabelCreate(LabelSchema):
    pass


class LabelUpdate(LabelSchema):
    pass


class Label(LabelSchema):
    label_id: int = None

    class Config:
        orm_mode = True
