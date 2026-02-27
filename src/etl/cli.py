from __future__ import annotations

import sys
from datetime import datetime

from src.etl.client import SourceAPIClient
from src.etl.service import ETLService
from src.etl.transformer import DataTransformer
from src.target_db.repository import TargetRepository
from src.target_db.session import SessionLocal, init_db


def main(argv: list[str] | None = None) -> None:
    args = argv if argv is not None else sys.argv[1:]
    if len(args) != 1:
        raise SystemExit("Usage: python -m src.etl.cli YYYY-MM-DD")

    date_str = args[0]
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError as exc:
        raise SystemExit("Date must be in format YYYY-MM-DD") from exc

    init_db()

    session = SessionLocal()
    try:
        client = SourceAPIClient()
        transformer = DataTransformer()
        repository = TargetRepository(session=session)
        service = ETLService(client=client, transformer=transformer, repository=repository)
        service.run(date)
    finally:
        session.close()


if __name__ == "__main__":
    main()

