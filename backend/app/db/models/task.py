from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, CompanyScopedMixin, TimestampMixin, UUIDPrimaryKeyMixin


class Task(Base, UUIDPrimaryKeyMixin, CompanyScopedMixin, TimestampMixin):
    __tablename__ = "tasks"

    owner_role_id: Mapped[uuid.UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("roles.id", ondelete="SET NULL"), nullable=True, index=True
    )
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    detail: Mapped[str | None] = mapped_column(Text, nullable=True)
    okr_ref: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="todo")
    priority: Mapped[str] = mapped_column(String(20), nullable=False, default="medium")
    due_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    depends_on: Mapped[list[uuid.UUID] | None] = mapped_column(ARRAY(PG_UUID(as_uuid=True)), nullable=True)
    source: Mapped[str] = mapped_column(String(30), nullable=False, default="human")
