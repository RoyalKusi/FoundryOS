from __future__ import annotations

import uuid

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Message(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "messages"

    thread_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("threads.id", ondelete="CASCADE"), nullable=False, index=True
    )
    author_member_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("members.id", ondelete="SET NULL"), nullable=True
    )
    kind: Mapped[str] = mapped_column(String(30), nullable=False, default="text")
    body: Mapped[str | None] = mapped_column(Text, nullable=True)
    attachments: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    citations: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
