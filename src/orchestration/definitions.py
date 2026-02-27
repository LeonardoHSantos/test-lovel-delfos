from __future__ import annotations

from dagster import Definitions

from src.orchestration.assets import daily_energy_etl
from src.orchestration.jobs import daily_etl_job
from src.orchestration.resources import source_db, target_db
from src.orchestration.schedules import daily_etl_schedule


defs = Definitions(
    assets=[daily_energy_etl],
    resources={
        "source_db": source_db,
        "target_db": target_db,
    },
    jobs=[daily_etl_job],
    schedules=[daily_etl_schedule],
)

