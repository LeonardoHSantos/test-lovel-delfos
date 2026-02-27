from __future__ import annotations

from dagster import define_asset_job

from src.orchestration.assets import daily_energy_etl


daily_etl_job = define_asset_job(
    "daily_energy_etl_job",
    selection=[daily_energy_etl],
)

