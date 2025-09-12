import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from langchain_community.utilities.sql_database import SQLDatabase


def get_db():
    with sqlite3.connect("data/processed/fraudDB.db", check_same_thread=False) as con:
        engine = create_engine(
            "sqlite:///",
            creator=lambda: con,
            poolclass=StaticPool,
            connect_args={"check_same_thread": False},
        )
    return SQLDatabase(engine)