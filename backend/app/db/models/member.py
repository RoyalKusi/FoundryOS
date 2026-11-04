from __future__ import annotations

import uuid

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, CompanyScopedMixin, TimestampMixin, UUIDPrimaryKeyMixin


class Member(Base, UUIDPrimaryKeyMixin, CompanyScopedMixin, TimestampMixin):
    __tablename__ = "members"

    kind: Mapped[str] = mapped_column(String(20), nullable=False)  # human|ai
    user_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    role_id: Mapped[uuid.UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    display_name: Mapped[str] = mapped_column(String(255), nullable=False)
    avatar: Mapped[str | None] = mapped_column(String(512), nullable=True)
