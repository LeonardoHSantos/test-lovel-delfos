from __future__ import annotations

from datetime import datetime

import pandas as pd

from src.etl.client import SourceAPIClient
from src.etl.transformer import DataTransformer
from src.target_db.repository import TargetRepository


class ETLService:
    def __init__(
        self,
        client: SourceAPIClient,
        transformer: DataTransformer,
        repository: TargetRepository,
    ) -> None:
        self._client = client
        self._transformer = transformer
        self._repository = repository

    def run(self, date: datetime) -> None:
        raw_df = self._client.fetch_day(date)
        if raw_df.empty:
            return

        aggregated = self._transformer.aggregate_10min(raw_df)
        if aggregated.empty:
            return

        # Garante que os sinais existem e obtem o mapa nome->id
        self._repository.ensure_signals()
        mapping = self._repository.get_signal_mapping()

        def map_signal(row: pd.Series) -> int:
            name = str(row["signal_name"])
            if name not in mapping:
                raise KeyError(f"Signal '{name}' not found in target mapping")
            return mapping[name]

        aggregated["signal_id"] = aggregated.apply(map_signal, axis=1)

        final_df = aggregated[["timestamp", "signal_id", "value"]]
        self._repository.bulk_insert(final_df)

