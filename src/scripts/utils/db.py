import os
import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from langchain_community.utilities.sql_database import SQLDatabase

def get_db():
    base_dir = os.path.dirname(os.path.dirname(__file__))  # go up from utils to src
    db_path = os.path.join(base_dir, "..", "data", "processed", "fraudDB.db")

    with sqlite3.connect(db_path, check_same_thread=False) as con:
        engine = create_engine(
            "sqlite:///",
            creator=lambda: con,
            poolclass=StaticPool,
            connect_args={"check_same_thread": False},
        )
    return SQLDatabase(engine)