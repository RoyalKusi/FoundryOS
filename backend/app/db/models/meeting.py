from __future__ import annotations
from typing import Any

import uuid

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, CompanyScopedMixin, TimestampMixin, UUIDPrimaryKeyMixin


class Meeting(Base, UUIDPrimaryKeyMixin, CompanyScopedMixin, TimestampMixin):
    __tablename__ = "meetings"

    thread_id: Mapped[uuid.UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("threads.id", ondelete="SET NULL"), nullable=True
    )
    agenda: Mapped[str | None] = mapped_column(Text, nullable=True)
    participants: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="scheduled")
    resolutions: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
