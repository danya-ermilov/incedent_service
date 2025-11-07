import uuid
import datetime
from pydantic import BaseModel, Field
from app.models import SourceEnum, StatusEnum


class IncidentCreate(BaseModel):
    description: str = Field(..., min_length=1)
    status: StatusEnum = Field(StatusEnum.new)
    source: SourceEnum


class IncidentRead(BaseModel):
    id: uuid.UUID
    description: str
    status: StatusEnum
    source: SourceEnum
    created_at: datetime.datetime

    class Config:
        orm_mode = True


class IncidentUpdate(BaseModel):
    status: StatusEnum
