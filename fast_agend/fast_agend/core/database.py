from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = "postgresql+psycopg2://AGEND:postgres@localhost:5434/postgres_db"

engine = create_engine(
    DATABASE_URL,
    echo=True  # log das queries (desligar em produção)
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

class Base(DeclarativeBase):
    pass
