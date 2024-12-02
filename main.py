"""main program"""

import bcrypt
import customtkinter as ctk
from rich.console import Console
from modules.service import ctk_init, make_label, make_btn, make_entry
from modules.connection import session
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
        return bcrypt.checkpw(
            entry.encode("utf-8"), hashed_password=record
        )

    def insert_to_db(self, email: str, password: str):
        """zaznam do DB"""
        bank_user = BankUser(password=password, email=email)
        with session.connection():
            session.add(bank_user)


if __name__ == "__main__":
    app: App = App()
    app.mainloop()
