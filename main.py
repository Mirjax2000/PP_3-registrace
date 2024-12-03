"""main program"""

import bcrypt
import customtkinter as ctk
from rich.console import Console
from modules.service import ctk_init, make_label, make_btn, make_entry
from modules.connection import session
from sqlalchemy import text
from models.model import BankUser

csl: Console = Console()


class App(ctk.CTk):
    """Main app"""

    def __init__(self):
        super().__init__()
        ctk_init(self, "registration", 400, 400)

    @staticmethod
    def encrypt(password: str) -> bytes:
        """encription"""
        return bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        )

    @staticmethod
    def verifikace(entry: str, record: bytes) -> bool:
        """Verifikace vstupu"""
        return bcrypt.checkpw(entry.encode("utf-8"), record)

    @staticmethod
    def insert_to_db(email: str, password: str) -> None:
        """zaznam do DB"""
        hash_password: bytes = App.encrypt(password)
        bank_user = BankUser(password=hash_password, email=email)
        with session.connection():
            session.add(bank_user)
            csl.log("Zaznam pridan.", style="bold blue")
            session.commit()

    def hash_from_db(self, email: str):
        """Ziskej hash z DB"""
        with session.connection():
            result = session.query(BankUser).filter(
                BankUser.email == email
            )
            if result:
                csl.log(result)
            else:
                csl.log("Zaznam nenalezen!", style="bold red")


if __name__ == "__main__":
    csl.clear()
    app: App = App()
    app.mainloop()
