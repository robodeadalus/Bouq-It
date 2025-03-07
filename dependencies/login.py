import streamlit as st
import streamlit_authenticator.controllers as stauth
from database import User
from sqlalchemy import select
import database as db

class login_flow:
    def __init__(self, db: db.Session):
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
