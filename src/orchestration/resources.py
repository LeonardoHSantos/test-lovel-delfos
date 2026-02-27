from __future__ import annotations

from collections.abc import Iterator

from dagster import resource
from sqlalchemy.orm import Session

from src.source_api.db import SessionLocal as SourceSessionLocal
from src.target_db.session import SessionLocal as TargetSessionLocal, init_db as init_target_db


@resource
def source_db() -> Iterator[Session]:
    session = SourceSessionLocal()
    try:
        yield session
    finally:
        session.close()


@resource
def target_db() -> Iterator[Session]:
    init_target_db()
    session = TargetSessionLocal()
    try:
        yield session
    finally:
        session.close()

