# Energy ETL Pipeline

Este repositório implementa um pipeline de ETL para dados de energia, com:

- Banco de dados **Fonte** em PostgreSQL
- API **FastAPI** expondo os dados do banco fonte
- Banco de dados **Alvo** modelado com **SQLAlchemy ORM**
- Processo de ETL utilizando **httpx** + **pandas**
- Orquestração com **Dagster**
- Ambiente totalmente containerizado com **Docker** e **Docker Compose**

Instruções completas de setup, execução e decisões técnicas serão detalhadas conforme as próximas etapas forem implementadas.

Atualmente, o banco de dados Fonte é populado com dados sintéticos com frequência 1-minutal, cobrindo o período de\
**2024-01-01 00:00:00** até **2024-01-10 23:59:00** (10 dias consecutivos).