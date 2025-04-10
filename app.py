import streamlit as st

import dependencies.login as auth
from dependencies.database import *
from dependencies.login import auth_flow

if "db" not in st.session_state or "engine" not in st.session_state:
    st.session_state["engine"], st.session_state["db"] = db_connect()
if "auth" not in st.session_state:
    st.session_state["auth"] = auth.auth_flow(db=st.session_state["db"])
else:
    authenticator: auth_flow = st.session_state["auth"]

# ---- PAGE SETUP ----

pages = [
    st.Page(
        page="pages/homepage.py",
        title="Home Page",
        icon=":material/home:",
        default=True,
    ),
    st.Page(
        page="pages/catalogue.py",
        title="Flower Catalogue",
        icon=":material/local_florist:",
    ),
    st.Page(
        page="pages/shop_catalogue.py",
        title="Shop Catalogue",
        icon=":material/storefront:",
    ),
    st.Page(
        page="pages/locator.py",
        title="Flower Shop Locator",
        icon=":material/pin_drop:",
    ),
    st.Page(
        page="pages/order.py",
        title="Order Page",
        icon=":material/shopping_cart:",
    ),
    st.Page(
        page="pages/language_of_flowers.py",
        title="Language of Flowers",
        icon=":material/auto_stories:",
    ),
    # Placeholder for easy access, remove once fully implemented
    st.Page(page="pages/custombouquet.py", title="Custom Bouquets"),
    st.Page(
        page="pages/checkout.py",
        title="Checkout Page",
    ),
    st.Page(
        page="pages/mycart.py",
        title="My Cart",
    ),
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
                st.switch_page("pages/mycart.py")
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
    div[data-testid="stSidebarUserContent"] {
        display: flex;
        margin-top: auto;
        padding-bottom: 1.5rem;
    }
    div[data-testid="stSidebarContent"] {
        display: flex;
        flex-direction: column;
    }
    [data-testid="stElementToolbar"]{
        visibility: hidden;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)
