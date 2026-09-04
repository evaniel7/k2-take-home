import uuid
from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import Column, String, Integer, Text, DateTime, Enum, Uuid

from app.database import Base


class RequestStatus(str, PyEnum):
    NEW = "new"
    ACCEPTED = "accepted"
    DEFERRED = "deferred"
    DECLINED = "declined"


class Request(Base):
    __tablename__ = "requests"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    problem_statement = Column(Text, nullable=False)
    expected_impact = Column(Text, nullable=False)
    urgency = Column(Integer, nullable=False)
    status = Column(Enum(RequestStatus), default=RequestStatus.NEW, nullable=False)
    decision_reason = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at = Column(DateTime, nullable=True)
