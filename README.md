# Energy ETL Pipeline

Este repositório implementa um pipeline de ETL para dados de energia, com:

- Banco de dados **Fonte** em PostgreSQL
- API **FastAPI** expondo os dados do banco fonte
- Banco de dados **Alvo** modelado com **SQLAlchemy ORM**
- Processo de ETL utilizando **httpx** + **pandas**
- Orquestração com **Dagster**
- Ambiente totalmente containerizado com **Docker** e **Docker Compose**

Instruções completas de setup, execução e decisões técnicas serão detalhadas conforme as próximas etapas forem implementadas.