"""DB model"""

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer, LargeBinary
from rich.console import Console
from modules.connection import engine

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
    csl.print(f"Vytvarim table: {name}.", style="bold blue")

    Base.metadata.create_all(engine)
    csl.print(f"table: {name} vytvoren.", style="Bold Blue")


if __name__ == "__main__":
    create_tables(table_name)
