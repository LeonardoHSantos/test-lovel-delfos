from __future__ import annotations

from typing import Dict

import pandas as pd
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from src.target_db.models import DataPoint, Signal


PREDEFINED_SIGNALS = [
    "wind_speed_mean",
    "wind_speed_min",
    "wind_speed_max",
    "wind_speed_std",
    "power_mean",
    "power_min",
    "power_max",
    "power_std",
]


class TargetRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def ensure_signals(self) -> None:
        for name in PREDEFINED_SIGNALS:
            stmt = insert(Signal).values(name=name).on_conflict_do_nothing(index_elements=["name"])
            self._session.execute(stmt)
        self._session.commit()

    def get_signal_mapping(self) -> Dict[str, int]:
        stmt = select(Signal)
        rows = self._session.execute(stmt).scalars().all()
        return {row.name: row.id for row in rows}

    def bulk_insert(self, df: pd.DataFrame) -> None:
        records = df.to_dict(orient="records")
        objects = [
            DataPoint(timestamp=row["timestamp"], signal_id=row["signal_id"], value=row["value"])
            for row in records
        ]
        self._session.bulk_save_objects(objects)
        self._session.commit()

