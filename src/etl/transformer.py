from __future__ import annotations

from typing import List

import pandas as pd


class DataTransformer:
    def aggregate_10min(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df

        # Garantir colunas esperadas
        for col in ("wind_speed", "power"):
            if col not in df.columns:
                df[col] = pd.NA

        agg = df.resample("10min").agg(
            {
                "wind_speed": ["mean", "min", "max", "std"],
                "power": ["mean", "min", "max", "std"],
            }
        )

        # Flatten de colunas multi-nível
        agg.columns = [f"{col}_{stat}" for col, stat in agg.columns.to_flat_index()]
        agg = agg.reset_index()  # timestamp volta para coluna

        # Normalizar para formato long: timestamp, signal_name, value
        value_vars: List[str] = list(agg.columns)
        value_vars.remove("timestamp")

        melted = agg.melt(
            id_vars=["timestamp"],
            value_vars=value_vars,
            var_name="signal_name",
            value_name="value",
        )

        # Remover linhas totalmente vazias (pode ocorrer se alguma coluna vier vazia)
        melted = melted.dropna(subset=["value"])

        return melted

