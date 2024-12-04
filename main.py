"""main program"""

from typing import Any, TypeAlias
import bcrypt
import customtkinter as ctk
from rich.console import Console
from modules.service import (
    ctk_init,
    mk_lbl,
    mk_btn,
    mk_entr,
    mk_frm,
)
from modules.connection import session
from models.model import BankUser

csl: Console = Console()
Lbl: TypeAlias = ctk.CTkLabel
Entr: TypeAlias = ctk.CTkEntry
Btn: TypeAlias = ctk.CTkButton
Frm: TypeAlias = ctk.CTkFrame


class App(ctk.CTk):
    """Main app"""

    def __init__(self):
        super().__init__()
        ctk_init(self, "registration a prihlseni", 400, 600)

        self.rowconfigure((0, 1), weight=1, uniform="a")
        self.columnconfigure(0, weight=1, uniform="a")

        self.reg_frame: Frm = mk_frm(
            self,
            {},
            {
                "row": 0,
                "column": 0,
                "padx": 5,
                "pady": 5,
            },
        )
        #
        self.reg_frame.columnconfigure(0, weight=0, uniform="a")
        self.reg_frame.columnconfigure(1, weight=1, uniform="b")
        #

        self.header_lb: Lbl = mk_lbl(
            self.reg_frame,
            {"text": "Registrace"},
            {
                "row": 0,
                "column": 0,
                "columnspan": 2,
                "pady": 10,
            },
        )
        self.email_lb_reg: Lbl = mk_lbl(
            self.reg_frame,
            {"text": "Email:"},
            {"row": 1, "column": 0, "pady": 5, "padx": (10, 0)},
        )
        self.heslo_lb_reg: Lbl = mk_lbl(
            self.reg_frame,
            {"text": "Heslo:"},
            {"row": 2, "column": 0, "pady": 5, "padx": (10, 0)},
        )
        #
        self.email_ent_reg: Entr = mk_entr(
            self.reg_frame,
            {"placeholder_text": " ..."},
            {"row": 1, "column": 1, "pady": 5, "padx": 10},
        )
        self.heslo_ent_reg: Entr = mk_entr(
            self.reg_frame,
            {"placeholder_text": " ..."},
            {"row": 2, "column": 1, "pady": 5, "padx": 10},
        )
        self.reg_btn: Btn = mk_btn(
            self.reg_frame,
            {
                "text": "Zaregistrovat",
                "command": lambda: self.call_foo(
                    self.email_ent_reg.get(),
                    self.heslo_ent_reg.get(),
                ),
            },
            {
                "row": 3,
                "column": 0,
                "columnspan": 2,
                "pady": 20,
                "padx": 120,
            },
        )

        self.prihlas_frame: Frm = mk_frm(
            self,
            {},
            {
                "row": 1,
                "column": 0,
                "padx": 5,
                "pady": (0, 5),
            },
        )
        #
        self.prihlas_frame.columnconfigure(0, weight=0, uniform="a")
        self.prihlas_frame.columnconfigure(1, weight=1, uniform="b")
        #
        self.header: Lbl = mk_lbl(
            self.prihlas_frame,
            {"text": "Prihlaseni"},
            {
                "row": 0,
                "column": 0,
                "columnspan": 2,
                "pady": 10,
            },
        )

        self.email_lb_prihlas: Lbl = mk_lbl(
            self.prihlas_frame,
            {"text": "Email:"},
            {"row": 1, "column": 0, "pady": 5, "padx": (10, 0)},
        )
        self.heslo_lb_prihlas: Lbl = mk_lbl(
            self.prihlas_frame,
            {"text": "Heslo:"},
            {"row": 2, "column": 0, "pady": 5, "padx": (10, 0)},
        )
        #
        self.email_ent_prihlas: Entr = mk_entr(
            self.prihlas_frame,
            {"placeholder_text": " ..."},
            {"row": 1, "column": 1, "pady": 5, "padx": 10},
        )
        self.heslo_ent_prihlas: Entr = mk_entr(
            self.prihlas_frame,
            {"placeholder_text": " ..."},
            {"row": 2, "column": 1, "pady": 5, "padx": 10},
        )
        self.prihlas_btn: Btn = mk_btn(
            self.prihlas_frame,
            {
                "text": "Prihlasit",
                "command": lambda: self.prihlaseni(
                    self.email_ent_prihlas.get(),
                    self.heslo_ent_prihlas.get(),
                ),
            },
            {
                "row": 3,
                "column": 0,
                "columnspan": 2,
                "pady": 20,
                "padx": 120,
            },
        )
        self.info_reg: Lbl = mk_lbl(
            self.reg_frame,
            {
                "text": "Zaznam pridan",
                "text_color": ("green", "green"),
            },
            {
                "row": 4,
                "column": 0,
                "columnspan": 2,
            },
        )
        self.info_reg.grid_remove()

        self.info_prihlas: Lbl = mk_lbl(
            self.prihlas_frame,
            {},
            {
                "row": 4,
                "column": 0,
                "columnspan": 2,
            },
        )
        self.info_prihlas.grid_remove()

    def call_foo(self, email: str, password: str) -> None:
        """Volej funkci"""
        Tools.insert_to_db(email, password)
        self.update()

    def update(self) -> None:
        """update"""
        self.email_ent_reg.delete("0", "end")
        self.heslo_ent_reg.delete("0", "end")
        self.info_reg.grid()
        self.update_idletasks()

    def prihlaseni(self, mail: str, password: str):
        """prihlaseni"""
        hash_pwd: Any = Tools.hash_from_db(mail)
        str_pwd: str = password
        self.info_prihlas.grid()

        if hash_pwd != "Zaznam nenalezen!":
            result = Tools.verifikace(str_pwd, hash_pwd)
            if result:
                self.info_prihlas.configure(
                    text="Prihlaseni v poradku",
                    text_color="#2c90fb",
                )
            else:
                self.info_prihlas.configure(
                    text="Spatne heslo!",
                    text_color="#ff7700",
                )
            self.update_idletasks()
        else:
            self.info_prihlas.configure(
                text="Email nenalezen!",
                text_color="#ff7700",
            )
            self.update_idletasks()


class Tools:
    """metody a funkce"""

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
        hash_password: bytes = Tools.encrypt(password)
        bank_user = BankUser(password=hash_password, email=email)
        with session.connection():
            session.add(bank_user)
            csl.log("Zaznam pridan.", style="bold blue")
            session.commit()

    @staticmethod
    def hash_from_db(email: str) -> Any | str:
        """Ziskej hash z DB"""
        with session.connection():
            result: BankUser | None = (
                session.query(BankUser)
                .filter(BankUser.email == email)
                .first()
            )
            if result:
                vystup = result.password
                return vystup

            return "Zaznam nenalezen!"


if __name__ == "__main__":
    csl.clear()
    app: App = App()
    app.mainloop()
