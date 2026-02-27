# Energy ETL Pipeline

Este repositório implementa um pipeline de ETL para dados de energia, com:

- Banco de dados **Fonte** em PostgreSQL
- API **FastAPI** expondo os dados do banco fonte
- Banco de dados **Alvo** modelado com **SQLAlchemy ORM**
- Processo de ETL utilizando **httpx** + **pandas**
- Orquestração com **Dagster**
- Ambiente totalmente containerizado com **Docker** e **Docker Compose**

Atualmente, o banco de dados Fonte é populado com dados sintéticos com frequência 1-minutal, cobrindo o período de\
**2024-01-01 00:00:00** até **2024-01-10 23:59:00** (10 dias consecutivos).

## Como rodar

- **1. Crie seu `.env`** a partir de `.env.example`:
  - Copie `.env.example` para `.env` e ajuste variáveis se necessário.
- **2. Suba os serviços com Docker Compose**:
  - `cd docker`
  - `docker compose up --build`
- **3. Popule o banco Fonte**:
  - Em outro terminal, execute o script `scripts/seed_source_data.py` (por exemplo, usando `docker exec` em `postgres_source` ou rodando localmente com acesso ao banco).
- **4. Execute o ETL manualmente (opcional)**:
  - `python -m src.etl.cli 2024-01-01`
- **5. Orquestração Dagster**:
  - Acesse o Dagster Webserver em `http://localhost:3000` para materializar o asset diário `daily_energy_etl` ou deixar o `dagster-daemon` disparar conforme o schedule.

Mais detalhes de arquitetura e decisões técnicas podem ser incrementados conforme a evolução do projeto.