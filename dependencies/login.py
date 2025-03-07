from typing import Iterable, Optional

import sqlalchemy as sql
import streamlit as st
import streamlit_authenticator.controllers as stauth
from sqlalchemy import Sequence, String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, exc, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "customers"

    user_id: Mapped[int] = mapped_column(
        Sequence("customers_user_id_seq"), primary_key=True, unique=True
    )
    user_username: Mapped[str] = mapped_column(String(255), unique=True)
    user_email: Mapped[str] = mapped_column(String(255))
    user_password: Mapped[str] = mapped_column(String(255))
    user_salt: Mapped[str] = mapped_column(String(255))
    last_name: Mapped[str] = mapped_column(String(255))
    first_name: Mapped[str] = mapped_column(String(255))
    middle_name: Mapped[Optional[str]]
    user_address: Mapped[str] = mapped_column(String(255))
    user_barangay: Mapped[str] = mapped_column(String(255))
    user_city: Mapped[str] = mapped_column(String(255))
    user_zipcode: Mapped[str] = mapped_column(String(255))

    def __repr__(self) -> str:
        return f"User(id={self.user_id!r})"


class login_flow:
    def __init__(self, db: Session):
        self.db = db
        self.credentials = self.get_credentials()
        self.authenticator = stauth.AuthenticationController(
            credentials=self.credentials
        )

    def get_credentials(self) -> dict:
        db = self.db

        credentials = {"usernames": {}}

        users = select(
            User.first_name,
            User.last_name,
            User.user_username,
            User.user_email,
            User.user_password,
            User.user_salt,
        )

        for f, l, u, e, p, s in db.execute(users):
            credentials["usernames"] |= {
                u: {
                    "email": e,
                    "failed_login_attempts": 0,
                    "first_name": f,
                    "last_name": l,
                    "logged_in": False,
                    "password": p + s,
                }
            }

        return credentials

    @st.dialog("Login")
    def login(self):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Submit"):
            if self.authenticator.login(username=username, password=password):
                st.rerun()
            else:
                st.error("Incorrect Credentials")
            print(st.session_state["authentication_status"])
