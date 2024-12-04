"""DB model"""

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer, LargeBinary, text
from rich.console import Console
from modules.connection import engine, session

csl: Console = Console()
Base = declarative_base()

table_name: str = "bank_users"


class BankUser(Base):
    """vytvareni tablu"""

    __tablename__: str = table_name

    user_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        unique=True,
    )
    password = Column(LargeBinary, nullable=False)
    email = Column(String(255), nullable=False, unique=True)

    def __repr__(self) -> str:
        return f"email: {self.email}."

    def __str__(self) -> str:
        return f"ID: {self.user_id}, Email: {self.email}"


def create_tables(name: str):
    """Vytvori tably v DB: health"""
    csl.log(f"Vytvarim table: {name}.", style="bold blue")
    Base.metadata.create_all(engine)
    csl.log(f"table: {name} vytvoren.", style="Bold Blue")


def table_list() -> list:
    """vypis tabulek z databaze"""
    with session.connection():
        vypis = session.execute(
            text(
                "SELECT table_name FROM information_schema.tables\
                                      WHERE table_schema = 'public';"
            )
        ).fetchmany()
        tables: list = (
            [row[0] for row in vypis]
            if vypis
            else ["Zadna tabulka nenalezena!"]
        )
        return tables


if __name__ == "__main__":
    csl.clear()
    create_tables(table_name)
    csl.log(*table_list())
