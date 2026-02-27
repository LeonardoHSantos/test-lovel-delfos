from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict

import httpx
import pandas as pd

from src.settings import get_settings


class SourceAPIClient:
    def __init__(self, base_url: str | None = None) -> None:
        settings = get_settings()
        if base_url is None:
            base_url = f"http://{settings.api_host}:{settings.api_port}"
        self._base_url = base_url.rstrip("/")

    def fetch_day(self, date: datetime) -> pd.DataFrame:
        start = datetime(date.year, date.month, date.day)
        end = start + timedelta(days=1)

        params: Dict[str, Any] = {
            "start_date": start.isoformat(),
            "end_date": end.isoformat(),
            "variables": ["wind_speed", "power"],
        }

        with httpx.Client(base_url=self._base_url, timeout=30.0) as client:
            response = client.get("/data", params=params)
            response.raise_for_status()
            data = response.json()

        df = pd.DataFrame(data)
        if df.empty:
            return df

        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df.set_index("timestamp").sort_index()
        return df

