from __future__ import annotations

import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, CompanyScopedMixin, TimestampMixin, UUIDPrimaryKeyMixin


class Thread(Base, UUIDPrimaryKeyMixin, CompanyScopedMixin, TimestampMixin):
    __tablename__ = "threads"

    type: Mapped[str] = mapped_column(String(30), nullable=False, default="direct")
    title: Mapped[str | None] = mapped_column(String(255), nullable=True)


class ThreadParticipant(Base, TimestampMixin):
    __tablename__ = "thread_participants"

    thread_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("threads.id", ondelete="CASCADE"), primary_key=True
    )
    member_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("members.id", ondelete="CASCADE"), primary_key=True
    )
