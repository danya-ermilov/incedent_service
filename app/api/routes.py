from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession


from app.schemas import (
    IncidentCreate,
    IncidentRead,
    IncidentUpdate,
    StatusEnum,
)

from app.db.session import get_session
from app import crud


router = APIRouter()


@router.post("/incidents", response_model=IncidentRead, status_code=status.HTTP_201_CREATED)
async def create_incident_endpoint(
    payload: IncidentCreate,
    db: AsyncSession = Depends(get_session)
):
    incident = await crud.create_incident(db, payload)
    return incident


@router.get("/incidents", response_model=List[IncidentRead])
async def list_incidents_endpoint(
    status: Optional[StatusEnum] = Query(None, description="Фильтр по статусу"),
    db: AsyncSession = Depends(get_session),
):
    items = await crud.list_incidents(db, status=status)
    return items


@router.patch("/incidents/{incident_id}/status", response_model=IncidentRead)
async def update_status_endpoint(
    incident_id: UUID,
    payload: IncidentUpdate,
    db: AsyncSession = Depends(get_session),
):
    updated = await crud.update_incident_status(db, incident_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Incident not found")
    return updated
