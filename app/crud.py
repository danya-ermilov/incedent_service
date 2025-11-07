from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Incident
from app.schemas import (
    IncidentCreate,
    IncidentUpdate,
    StatusEnum,
)
import uuid


async def create_incident(
    db: AsyncSession,
    payload: IncidentCreate
) -> Incident:
    obj = Incident(
        description=payload.description,
        status=payload.status,
        source=payload.source,
    )
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


async def list_incidents(
    db: AsyncSession,
    status: Optional[StatusEnum] = None,
) -> List[Incident]:
    query = select(Incident)
    if status:
        query = query.where(Incident.status == status)
    result = await db.execute(query)
    return result.scalars().all()


async def get_incident(
    db: AsyncSession,
    incident_id: uuid.UUID,
) -> Incident | None:
    return await db.get(Incident, incident_id)


async def update_incident_status(
    db: AsyncSession,
    incident_id: uuid.UUID,
    payload: IncidentUpdate
) -> Incident | None:
    obj = await get_incident(db, incident_id)
    if not obj:
        return None
    obj.status = payload.status
    await db.commit()
    await db.refresh(obj)
    return obj
