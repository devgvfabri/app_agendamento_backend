#################################################################################

* poetry new ______

* poetry install

-------------------------------------------------------------------------
|                                                                       |        
|    caminho: /projetos_apps/app_agendamento_backend/fast_agend         |
|    poetry shell para ativar ambiente virtual                          |
|    task run  --- roda o server                                        |
|                                                                       |
|    ou      uvicorn fast_agend.app:app --reload                        |        
|                                                                       |        
|                                                                       |
|                                                                       |
-------------------------------------------------------------------------

task test --- executa o teste

* Acessar o banco:
-  docker exec -it agend_db psql -U AGEND -d postgres_db

Executar migrações no banco:

1. poetry run alembic revision --autogenerate -m "create users table"

2. poetry run alembic upgrade head
