import re
from typing import Tuple

import streamlit as st
import streamlit_authenticator.controllers as stauth
from sqlalchemy import select
from streamlit_authenticator import Hasher

from dependencies.database import *


class auth_flow:
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
            User.username,
            User.email,
            User.password,
        )

        for f, l, u, e, p in db.execute(users).all():
            credentials["usernames"] |= {
                u: {
                    "email": e,
                    "failed_login_attempts": 0,
                    "first_name": f,
                    "last_name": l,
                    "logged_in": False,
                    "password": p,
                }
            }

        return credentials

    def refresh_credentials(self):
        self.credentials = self.get_credentials()
        self.authenticator = stauth.AuthenticationController(
            credentials=self.credentials
        )

    def encrypt(self, password: str) -> str:
        return Hasher.hash(password)

    def add_user(self, form: dict) -> bool:
        user = User(
            username=form["username"],
            email=form["email"],
            password=self.encrypt(form["password1"]),
            last_name=form["last_name"],
            first_name=form["first_name"],
            middle_name=form["middle_name"] if form["middle_name"] else None,
            contact=form["contact"],
            address=form["address1"],
            barangay=form["address2"],
            city=form["address3"],
            zipcode=form["address4"],
        )

        self.db.add(user)
        self.db.commit()
        self.db.close()
        print("added user to database")

    def unique_username(self, username: str) -> bool:
        usernames = list(self.credentials["usernames"].keys())
        if not (username in usernames) or not usernames:
            return True
        else:
            return False

    def validate_email(self, email: str) -> bool:
        valid = re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email)
        return valid

    def validate_password(self, password: str, confirmation: str) -> bool:
        return password == confirmation

    def validate_contact(self, contact: str) -> bool:
        return contact.isnumeric()

    def validate_form(self, form: dict) -> bool:
        valid = True
        error = ""
        if not self.unique_username(form["username"]):
            st.error("Username is taken.\n")
            valid = False
        if not self.validate_email(form["email"]):
            st.error("Please enter a valid e-mail.\n")
            valid = False
        if not self.validate_password(form["password1"], form["password2"]):
            st.error("Passwords do not match.\n")
            valid = False
        if not self.validate_contact(form["contact"]):
            st.error("Please enter a valid contact no.")
            valid = False
        return valid

    @st.dialog("Login")
    def login(self):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Submit"):
            self.refresh_credentials()
            if self.authenticator.login(username=username, password=password):
                st.rerun()
            else:
                st.error("Incorrect Credentials")

    @st.dialog("Register")
    def register(self):
        form = {
            "username": st.text_input("Username"),
            "email": st.text_input("Email"),
            "password1": st.text_input("Password", type="password"),
            "password2": st.text_input("Confirm Password", type="password"),
            "first_name": st.text_input("First Name"),
            "middle_name": st.text_input("Middle Name"),
            "last_name": st.text_input("Last Name"),
            "contact": st.text_input("Mobile No."),
            "address1": st.text_input("Address Details"),
            "address2": st.text_input("Barangay"),
            "address3": st.text_input("City"),
            "address4": st.text_input("Zip Code"),
        }
        if st.button("Submit"):
            if self.validate_form(form):
                self.add_user(form)
                st.rerun()

    def logout(self):
        self.authenticator.logout()
