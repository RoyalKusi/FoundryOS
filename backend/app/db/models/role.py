from __future__ import annotations

import uuid

from sqlalchemy import String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, CompanyScopedMixin, TimestampMixin, UUIDPrimaryKeyMixin


class Role(Base, UUIDPrimaryKeyMixin, CompanyScopedMixin, TimestampMixin):
    __tablename__ = "roles"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    mandate: Mapped[str | None] = mapped_column(Text, nullable=True)
    kpis: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    autonomy: Mapped[str] = mapped_column(String(20), nullable=False, default="autonomous")
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="proposed")
    human_member_id: Mapped[uuid.UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
