
* poetry new ______

* poetry install
      
Caminho: /projetos_apps/app_agendamento_backend/fast_agend
poetry shell para ativar ambiente virtual
| task run |  (roda o server) ou | uvicorn fast_agend.app:app --reload |      


task test --- executa o teste

* Acessar o banco:
-  docker exec -it agend_db psql -U AGEND -d postgres_db


Executar migrações no banco:

1. poetry run alembic revision --autogenerate -m "create users table"

2. poetry run alembic upgrade head

** É necessário apagar a tabela e versões antigas, caso for criar uma nova coluna que é necessário conter dados.

1. DROP TABLE table-name;
2. DROP TABLE alembic_version;

se o banco quebrar

1 Derrube o container e apague o volume do Postgres

docker compose down -v

suba o postgres
docker compose up -d

Confira o schema padrão
SHOW search_path;

deve ser
"$user", public


Apague TODAS as migrations locais
rm -rf fast_agend/alembic/versions/*
rm -rf fast_agend/alembic/__pycache__

Executar migrações no banco:

1. poetry run alembic revision --autogenerate -m "create users table"

2. poetry run alembic upgrade head