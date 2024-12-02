"""DB model"""

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer, Float
from rich.console import Console
from modules.connection import engine

console: Console = Console()
Base = declarative_base()


class Bmi(Base):
    """vytvareni tablu"""

    __tablename__ = "bmi"

    bmi_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        unique=True,
    )
    bmi_num = Column(Float, nullable=False)
    bmi_txt = Column(String(50), nullable=False)

    def __repr__(self):
        return f"bmi_id: {self.bmi_id}, bmi_number: {self.bmi_num}, bmi_text: {self.bmi_txt}."

    def __str__(self):
        return f"ID: {self.bmi_id}, BMI hodnota: {self.bmi_num} --> {self.bmi_txt}."


def create_tables(name: str):
    """Vytvori tably v DB: health"""
    console.print(f"Vytvarim table: {name}.", style="bold blue")

    Base.metadata.create_all(engine)
    console.print(f'table: {name} vytvoren.',style="Bold Blue")


if __name__ == "__main__":
    create_tables("bmi")
