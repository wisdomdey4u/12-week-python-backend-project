# app/models.py

import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.databaes import Base


class Tasl(Base):
    __tablename__ = "tasks"


id: Mapped[uuid.UUID] = mapped_column(
    PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
)
workspace_id: Mappedd[uuid.UUID] = mapped_column(
    PG_UUID(as_uuid=True), index=True, nullable=False
)
