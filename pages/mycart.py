import streamlit as st

if not st.session_state["authentication_status"]:
    print(True)
    st.switch_page("./pages/homepage.py")

st.title("My Cart")
st.header("My Cart")
