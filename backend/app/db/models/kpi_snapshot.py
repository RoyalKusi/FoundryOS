from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB, UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class KpiSnapshot(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "kpi_snapshots"

    role_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("roles.id", ondelete="CASCADE"), nullable=False, index=True
    )
    period: Mapped[str] = mapped_column(String(50), nullable=False)
    metrics: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    score: Mapped[float | None] = mapped_column(Float, nullable=True)
