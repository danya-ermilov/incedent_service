import uuid
import datetime
from enum import Enum as PyEnum

from sqlalchemy import Column, Text, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import declarative_base
from sqlalchemy import text

Base = declarative_base()


class SourceEnum(PyEnum):
    operator = "operator"
    monitoring = "monitoring"
    partner = "partner"


class StatusEnum(PyEnum):
    new = "new"
    in_progress = "in_progress"
    resolved = "resolved"
    closed = "closed"


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    description = Column(Text, nullable=False)
    status = Column(
        SQLEnum(StatusEnum, name="status_enum"),
        nullable=False,
        server_default=text(f"'{StatusEnum.new.value}'"),
    )
    source = Column(SQLEnum(SourceEnum, name="source_enum"), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.datetime.utcnow)

    def __repr__(self) -> str:
        return f"<Incident id={self.id} status={self.status} source={self.source}>"
