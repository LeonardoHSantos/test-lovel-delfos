from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.source_api.db import get_db
from src.source_api.models import SourceData
from src.source_api.schemas import AllowedVariable, DataPoint


router = APIRouter()


@router.get("/data", response_model=List[DataPoint])
def get_data(
    start_date: str = Query(..., description="Start datetime in ISO format"),
    end_date: str = Query(..., description="End datetime in ISO format"),
    variables: List[AllowedVariable] = Query(..., description="Variables to return"),
    db: Session = Depends(get_db),
    ) -> List[DataPoint]:
    from datetime import datetime

    try:
        start_dt = datetime.fromisoformat(start_date)
        end_dt = datetime.fromisoformat(end_date)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="start_date and end_date must be valid ISO datetime strings",
        ) from exc

    if end_dt <= start_dt:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="end_date must be greater than start_date",
        )

    if not variables:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one variable must be provided",
        )

    query = (
        select(SourceData)
        .where(SourceData.timestamp >= start_dt)
        .where(SourceData.timestamp < end_dt)
        .order_by(SourceData.timestamp)
    )

    rows = db.execute(query).scalars().all()

    result: List[DataPoint] = []
    for row in rows:
        result.append(
            DataPoint(
                timestamp=row.timestamp,
                wind_speed=row.wind_speed if "wind_speed" in variables else None,
                power=row.power if "power" in variables else None,
                ambient_temperature=row.ambient_temperature
                if "ambient_temperature" in variables
                else None,
            )
        )

    return result

