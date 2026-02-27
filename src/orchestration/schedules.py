from __future__ import annotations

from dagster import build_schedule_from_partitioned_job

from src.orchestration.jobs import daily_etl_job


daily_etl_schedule = build_schedule_from_partitioned_job(daily_etl_job)

