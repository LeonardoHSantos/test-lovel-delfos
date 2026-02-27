from __future__ import annotations

from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from sqlalchemy import create_engine

from src.settings import build_source_db_url
from src.source_api.db import Base
from src.source_api import models  # noqa: F401


START_DATE = datetime(2024, 1, 1)
DAYS = 10
FREQ = "1min"
RANDOM_SEED = 42


def generate_data() -> pd.DataFrame:
    rng = pd.date_range(start=START_DATE, end=START_DATE + timedelta(days=DAYS), freq=FREQ, inclusive="left")
    generator = np.random.default_rng(RANDOM_SEED)

    wind_speed = generator.uniform(0, 25, size=len(rng))
    power = generator.uniform(0, 5_000, size=len(rng))
    ambient_temperature = generator.uniform(-5, 45, size=len(rng))

    return pd.DataFrame(
        {
            "timestamp": rng,
            "wind_speed": wind_speed,
            "power": power,
            "ambient_temperature": ambient_temperature,
        }
    )


def main() -> None:
    engine = create_engine(build_source_db_url(), future=True)

    Base.metadata.create_all(bind=engine)

    df = generate_data()

    with engine.begin() as connection:
        connection.exec_driver_sql("TRUNCATE TABLE data")
        df.to_sql("data", con=connection, if_exists="append", index=False)


if __name__ == "__main__":
    main()

