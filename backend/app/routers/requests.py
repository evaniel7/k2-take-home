from datetime import datetime
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import desc, asc
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Request, RequestStatus
from app.schemas import (
    RequestCreate,
    RequestUpdate,
    RequestResponse,
    RequestListResponse,
    DecisionCreate,
    StatusUpdatePayload,
    BulkDeletePayload,
)

router = APIRouter(prefix="/requests", tags=["requests"])


@router.post("/", response_model=RequestResponse, status_code=201)
def create_request(request_data: RequestCreate, db: Session = Depends(get_db)):
    """Create a new request."""
    db_request = Request(**request_data.model_dump())
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request


@router.get("/deleted", response_model=RequestListResponse)
def list_deleted_requests(db: Session = Depends(get_db)):
    """List all soft-deleted requests."""
    query = db.query(Request).filter(Request.deleted_at.isnot(None))
    query = query.order_by(desc(Request.deleted_at))
    items = query.all()
    return RequestListResponse(items=items, total=len(items))


@router.post("/permanent-delete", status_code=204)
def bulk_permanent_delete(payload: BulkDeletePayload, db: Session = Depends(get_db)):
    """Permanently delete multiple requests."""
    for request_id in payload.ids:
        db_request = db.query(Request).filter(Request.id == request_id).first()
        if db_request:
            db.delete(db_request)
    db.commit()
    return None


@router.get("/", response_model=RequestListResponse)
def list_requests(
    status: Optional[RequestStatus] = Query(None, description="Filter by status"),
    urgency: Optional[int] = Query(None, ge=1, le=4, description="Filter by urgency"),
    sort_by: str = Query("created_at", description="Sort field"),
    sort_order: str = Query("desc", description="Sort order: asc or desc"),
    include_archived: bool = Query(False, description="Include declined requests"),
    db: Session = Depends(get_db),
):
    """List all requests with optional filtering and sorting."""
    query = db.query(Request).filter(Request.deleted_at.is_(None))

    # Filter by status
    if status:
        query = query.filter(Request.status == status)
    elif not include_archived:
        # By default, exclude declined requests (treated as archived)
        query = query.filter(Request.status != RequestStatus.DECLINED)

    # Filter by urgency
    if urgency:
        query = query.filter(Request.urgency == urgency)

    # Sorting
    sort_column = getattr(Request, sort_by, Request.created_at)
    if sort_order == "asc":
        query = query.order_by(asc(sort_column))
    else:
        query = query.order_by(desc(sort_column))

    items = query.all()
    return RequestListResponse(items=items, total=len(items))


@router.get("/archived", response_model=RequestListResponse)
def list_archived_requests(db: Session = Depends(get_db)):
    """List all archived (declined) requests."""
    query = db.query(Request).filter(
        Request.status == RequestStatus.DECLINED,
        Request.deleted_at.is_(None)
    )
    query = query.order_by(desc(Request.updated_at))
    items = query.all()
    return RequestListResponse(items=items, total=len(items))


@router.get("/{request_id}", response_model=RequestResponse)
def get_request(request_id: UUID, db: Session = Depends(get_db)):
    """Get a single request by ID."""
    db_request = db.query(Request).filter(
        Request.id == request_id,
        Request.deleted_at.is_(None)
    ).first()
    if not db_request:
        raise HTTPException(status_code=404, detail="Request not found")
    return db_request


@router.patch("/{request_id}", response_model=RequestResponse)
def update_request(
    request_id: UUID, request_data: RequestUpdate, db: Session = Depends(get_db)
):
    """Update a request."""
    db_request = db.query(Request).filter(Request.id == request_id).first()
    if not db_request:
        raise HTTPException(status_code=404, detail="Request not found")

    update_data = request_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_request, field, value)

    db.commit()
    db.refresh(db_request)
    return db_request


@router.post("/{request_id}/decision", response_model=RequestResponse)
def record_decision(
    request_id: UUID, decision: DecisionCreate, db: Session = Depends(get_db)
):
    """Record a decision on a request (accept, defer, or decline)."""
    db_request = db.query(Request).filter(Request.id == request_id).first()
    if not db_request:
        raise HTTPException(status_code=404, detail="Request not found")

    if db_request.status != RequestStatus.NEW:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot change decision. Request already has status: {db_request.status.value}",
        )

    db_request.status = decision.status
    db_request.decision_reason = decision.decision_reason
    db.commit()
    db.refresh(db_request)
    return db_request


@router.patch("/{request_id}/status", response_model=RequestResponse)
def update_status(
    request_id: UUID, payload: StatusUpdatePayload, db: Session = Depends(get_db)
):
    """Update the status of a request without requiring a reason."""
    db_request = db.query(Request).filter(Request.id == request_id).first()
    if not db_request:
        raise HTTPException(status_code=404, detail="Request not found")

    db_request.status = payload.status
    db.commit()
    db.refresh(db_request)
    return db_request


@router.delete("/{request_id}", status_code=204)
def delete_request(request_id: UUID, db: Session = Depends(get_db)):
    """Soft delete a request."""
    db_request = db.query(Request).filter(Request.id == request_id).first()
    if not db_request:
        raise HTTPException(status_code=404, detail="Request not found")

    db_request.deleted_at = datetime.utcnow()
    db.commit()
    return None


@router.delete("/{request_id}/permanent", status_code=204)
def permanent_delete_request(request_id: UUID, db: Session = Depends(get_db)):
    """Permanently delete a request."""
    db_request = db.query(Request).filter(Request.id == request_id).first()
    if not db_request:
        raise HTTPException(status_code=404, detail="Request not found")

    db.delete(db_request)
    db.commit()
    return None


@router.post("/{request_id}/restore", response_model=RequestResponse)
def restore_request(request_id: UUID, db: Session = Depends(get_db)):
    """Restore a soft-deleted request."""
    db_request = db.query(Request).filter(Request.id == request_id).first()
    if not db_request:
        raise HTTPException(status_code=404, detail="Request not found")

    if db_request.deleted_at is None:
        raise HTTPException(status_code=400, detail="Request is not deleted")

    db_request.deleted_at = None
    db.commit()
    db.refresh(db_request)
    return db_request
