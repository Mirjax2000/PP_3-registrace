"""Connection"""

import os
from dotenv import load_dotenv
from rich.console import Console
from sqlalchemy import Engine, text, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import (
    database_exists as db_exist,
    create_database as create_db,
)

console: Console = Console()
load_dotenv(override=True)

db_name: str = "bank"
db_url: str = (
    f"postgresql+psycopg://{os.getenv('USER')}:"
    f"{os.getenv('PASSWORD')}@{os.getenv('HOST')}:"
    f"{os.getenv('PORT')}/{db_name}"
)

engine: Engine = create_engine(db_url)

Session = sessionmaker(bind=engine)
session = Session()


def create_database(name: str):
    """Creating database"""
    console.clear()

    if not db_exist(engine.url):
        console.print(
            f"databaze neexistuje!\nVytvarim DB: {name}",
            style="red bold",
        )
        create_db(engine.url, encoding="utf-8")

        with session.connection() as conn:
            temp = conn.execute(text("SELECT version();"))
            console.print(temp.fetchone(), style="green")
            console.print("databaze vytvorena", style="blue")
    else:
        console.log("Databaze jiz existuje", style="blue")
        with session.connection() as conn:
            temp = conn.execute(text("SELECT version();"))
            console.print(temp.fetchone(), style="blue")


if __name__ == "__main__":
    create_database(db_name)
