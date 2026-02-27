from __future__ import annotations

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class Signal(Base):
    __tablename__ = "signal"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), unique=True, nullable=False, index=True)

    data_points = relationship("DataPoint", back_populates="signal", cascade="all, delete-orphan")


class DataPoint(Base):
    __tablename__ = "data"

    timestamp = Column(DateTime, primary_key=False, nullable=False, index=True)
    signal_id = Column(Integer, ForeignKey("signal.id"), primary_key=False, nullable=False, index=True)
    value = Column(Float, nullable=False)

    signal = relationship("Signal", back_populates="data_points")

    __table_args__ = (
        UniqueConstraint("timestamp", "signal_id", name="uq_data_timestamp_signal"),
    )

