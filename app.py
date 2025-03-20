import streamlit as st

import dependencies.login as auth
from dependencies.database import *
from dependencies.login import auth_flow

if "db" not in st.session_state:
    st.session_state["db"] = db_connect()
if "auth" not in st.session_state:
    st.session_state["auth"] = auth.auth_flow(db=st.session_state["db"])
else:
    authenticator: auth_flow = st.session_state["auth"]

# ---- PAGE SETUP ----

pages = [
    st.Page(
        page="views/homepage.py",
        title="Home Page",
        icon=":material/home:",
        default=True,
    ),
    st.Page(
        page="views/catalogue.py",
        title="Flower Catalogue",
        icon=":material/local_florist:",
    ),
    st.Page(
        page="views/locator.py",
        title="Flower Shop Locator",
        icon=":material/pin_drop:",
    ),
    st.Page(
        page="views/order.py",
        title="Order Page",
        icon=":material/shopping_cart:",
    ),
    st.Page(
        page="views/language_of_flowers.py",
        title="Language of Flowers",
        icon=":material/auto_stories:",
    ),
    # Placeholder for easy access, remove once fully implemented
    st.Page(
        page="views/checkout.py",
        title="Checkout Page",
    ),
    st.Page(
        page="views/mycart.py",
        title="My Cart",
    ),
    st.Page(
        page="views/myorders.py",
        title="My Orders",
    )
]

# ---- NAVIGATION SETUP ----
st.sidebar.image(
    "assets/Bouq-it.png",
    use_container_width=True,
)
pg = st.navigation(pages=pages)

with st.sidebar:
    auth = st.container(key="auth")
    with auth:
        if st.session_state["authentication_status"]:
            st.write(f"Hello {st.session_state['name']}")
            if st.button("View Cart", use_container_width=True):
                st.switch_page("views/mycart.py")
            if st.button("Logout", use_container_width=True):
                authenticator.logout()
                st.rerun()
        else:
            if st.button("Login", use_container_width=True):
                authenticator.login()
            if st.button("Register", use_container_width=True):
                authenticator.register()

# ---- RUN NAVIGATION ----
pg.run()

# ---- SHARED ON ALL views ----


custom_css = """
<style>
    .stSidebar span{
        color: white;
    }
    div[data-testid="stSidebarUserContent"] {
        display: flex;
        margin-top: auto;
        padding-bottom: 1.5rem;
    }
    .st-key-auth {
        color: white;
    }
    div[data-testid="stSidebarContent"] {
        display: flex;
        flex-direction: column;
    }
    [data-testid="stElementToolbar"]{
        visibility: hidden;
    }
    [data-testid="stTextInputRootElement"] input{
        color: white;
    }
    [data-testid="stTextInputRootElement"] button{
    color: white;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)
