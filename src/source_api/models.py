from __future__ import annotations

from sqlalchemy import Column, DateTime, Float

from src.source_api.db import Base


class SourceData(Base):
    __tablename__ = "data"

    timestamp = Column(DateTime, primary_key=True, index=True)
    wind_speed = Column(Float, nullable=False)
    power = Column(Float, nullable=False)
    ambient_temperature = Column(Float, nullable=False)

