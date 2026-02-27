from __future__ import annotations

from datetime import date, datetime

from dagster import DailyPartitionsDefinition, AssetExecutionContext, asset

from src.etl.client import SourceAPIClient
from src.etl.service import ETLService
from src.etl.transformer import DataTransformer
from src.target_db.repository import TargetRepository


daily_partitions = DailyPartitionsDefinition(start_date=date(2024, 1, 1))


@asset(partitions_def=daily_partitions, required_resource_keys={"target_db"})
def daily_energy_etl(context: AssetExecutionContext) -> None:
    partition_key = context.partition_key
    run_date = datetime.strptime(partition_key, "%Y-%m-%d")

    session = context.resources.target_db
    client = SourceAPIClient()
    transformer = DataTransformer()
    repository = TargetRepository(session=session)

    service = ETLService(client=client, transformer=transformer, repository=repository)
    service.run(run_date)

