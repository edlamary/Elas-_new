import os
from dotenv import load_dotenv
import sqlalchemy as sa #type: ignore
from sqlalchemy.engine import Engine #type: ignore

load_dotenv()

class Postgres():
    def __init__(self, database_name: str):
        host: str | None = os.getenv("POSTGRES_HOST")
        port: int = int(os.getenv("POSTGRES_PORT", "5432"))
        self.database: str | None = os.getenv("POSTGRES_DB")
        user: str | None = os.getenv("POSTGRES_USER")
        password: str | None = os.getenv("POSTGRES_PASSWORD")

        self.conn_string = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database_name}'
        self.engine: Engine = sa.create_engine(self.conn_string, pool_size=40, max_overflow=0, pool_timeout=5) #type: ignore
