"""main program"""

import base64
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
    def encrypt(password: str) -> str:
        """encription"""
        hash_bytes = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        )
        return base64.b64encode(hash_bytes).decode("utf-8")

    @staticmethod
    def verifikace(entry: str, record: str) -> bool:
        """Verifikace vstupu"""
        record_bytes: bytes = base64.b64decode(record)
        return bcrypt.checkpw(entry.encode("utf-8"), record_bytes)

    def insert_to_db(self, email: str, password: str) -> None:
        """zaznam do DB"""
        hash_password: str = App.encrypt(password)
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
    app: App = App()
    app.mainloop()
