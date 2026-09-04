from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from app.models import RequestStatus


class RequestCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    problem_statement: str = Field(..., min_length=1)
    expected_impact: str = Field(..., min_length=1)
    urgency: int = Field(..., ge=1, le=4)

    @field_validator("title", "problem_statement", "expected_impact")
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        return v.strip()


class RequestUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    problem_statement: Optional[str] = Field(None, min_length=1)
    expected_impact: Optional[str] = Field(None, min_length=1)
    urgency: Optional[int] = Field(None, ge=1, le=4)


class DecisionCreate(BaseModel):
    status: RequestStatus = Field(...)
    decision_reason: str = Field(..., min_length=1)

    @field_validator("status")
    @classmethod
    def status_must_be_decision(cls, v: RequestStatus) -> RequestStatus:
        if v == RequestStatus.NEW:
            raise ValueError("Cannot set status to 'new' as a decision")
        return v

    @field_validator("decision_reason")
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        return v.strip()


class StatusUpdatePayload(BaseModel):
    status: RequestStatus = Field(...)


class BulkDeletePayload(BaseModel):
    ids: list[UUID]


class RequestResponse(BaseModel):
    id: UUID
    title: str
    problem_statement: str
    expected_impact: str
    urgency: int
    status: RequestStatus
    decision_reason: Optional[str]
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]

    class Config:
        from_attributes = True


class RequestListResponse(BaseModel):
    items: list[RequestResponse]
    total: int
