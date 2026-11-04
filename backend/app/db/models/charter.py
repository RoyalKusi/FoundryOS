from __future__ import annotations
from typing import Any

import uuid
from datetime import datetime

from sqlalchemy import DateTime, Integer
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, CompanyScopedMixin, TimestampMixin, UUIDPrimaryKeyMixin


class Charter(Base, UUIDPrimaryKeyMixin, CompanyScopedMixin, TimestampMixin):
    __tablename__ = "charters"

    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    charter_json: Mapped[dict[str, Any]] = mapped_column("json", JSONB, nullable=False, default=dict)
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
