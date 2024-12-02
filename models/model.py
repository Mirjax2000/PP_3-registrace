"""DB model"""

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer
from rich.console import Console
from modules.connection import engine

console: Console = Console()
Base = declarative_base()

table_name: str = "bank_users"


class BankUser(Base):
    """vytvareni tablu"""

    __tablename__ = table_name

    user_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        unique=True,
    )
    password = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)

    def __repr__(self):
        return f"email: {self.email}, password: {self.password[:10]}."

    def __str__(self):
        return f"ID: {self.user_id}, Email: {self.email}, password: {self.password[:10]}"


def create_tables(name: str):
    """Vytvori tably v DB: health"""
    console.print(f"Vytvarim table: {name}.", style="bold blue")

    Base.metadata.create_all(engine)
    console.print(f"table: {name} vytvoren.", style="Bold Blue")


if __name__ == "__main__":
    create_tables(table_name)
