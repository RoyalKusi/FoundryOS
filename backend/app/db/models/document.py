from __future__ import annotations
from typing import Any

import uuid

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, TSVECTOR, UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, CompanyScopedMixin, TimestampMixin, UUIDPrimaryKeyMixin


class Document(Base, UUIDPrimaryKeyMixin, CompanyScopedMixin, TimestampMixin):
    __tablename__ = "documents"

    title: Mapped[str] = mapped_column(String(500), nullable=False)
    storage_path: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    mime_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    scope: Mapped[str] = mapped_column(String(100), nullable=False, default="company")
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="pending")
    doc_metadata: Mapped[dict[str, Any] | None] = mapped_column("metadata", JSONB, nullable=True)


class Chunk(Base, UUIDPrimaryKeyMixin, CompanyScopedMixin, TimestampMixin):
    __tablename__ = "chunks"

    document_id: Mapped[uuid.UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), nullable=True, index=True
    )
    scope: Mapped[str] = mapped_column(String(100), nullable=False, default="company")
    text: Mapped[str] = mapped_column(Text, nullable=False)
    embedding: Mapped[str | None] = mapped_column(Text, nullable=True)  # vector stored as text placeholder; pgvector handles real type in migration
    tsv: Mapped[str | None] = mapped_column(Text, nullable=True)
    chunk_metadata: Mapped[dict[str, Any] | None] = mapped_column("metadata", JSONB, nullable=True)
