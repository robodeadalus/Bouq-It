import streamlit as st

def register_user():
    with st.form(key="register", clear_on_submit=True):
        st.subheader("Sign Up")
        username = st.text_input("Username", placeholder= "Enter Your Username")
        email = st.text_input("Email", placeholder= "Enter Your Email")
        password = st.text_input("", placeholder= "Enter Your Password")
        password_confirm = st.text_input("", placeholder= "Confirm Your Password")

def validate_email():
    pass