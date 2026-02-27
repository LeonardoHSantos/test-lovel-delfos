from __future__ import annotations

from datetime import datetime
from typing import List, Literal

from pydantic import BaseModel, field_validator


AllowedVariable = Literal["wind_speed", "power", "ambient_temperature"]


class DataQuery(BaseModel):
    start_date: datetime
    end_date: datetime
    variables: List[AllowedVariable]

    @field_validator("end_date")
    @classmethod
    def check_dates(cls, v: datetime, values: dict) -> datetime:
        start = values.get("start_date")
        if start and v <= start:
            raise ValueError("end_date must be greater than start_date")
        return v


class DataPoint(BaseModel):
    timestamp: datetime
    wind_speed: float | None = None
    power: float | None = None
    ambient_temperature: float | None = None

