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

custom_css = """
<style>
    div[data-testid="stSidebarContent"] {
        display: flex;
        flex-direction: column;
    }
    div[data-testid="stSidebarUserContent"] {
        display: flex;
        flex-direction: column;
        flex-grow: 1;
        padding-bottom: 1.5rem;
    }
    div[data-testid="stSidebarUserContent"] > div > div[data-testid="stVerticalBlockBorderWrapper"]{
        height: 100%;
    }
    div[data-testid="stSidebarUserContent"] :not(div[data-testid]) {
        height: 100%;
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:has(> div > .st-key-nav){
        margin-bottom: auto;
    }
    [data-testid="stElementToolbar"]{
        visibility: hidden;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

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
    # HIDDEN PAGES
    st.Page(
        page="pages/custombouquet.py",
        title="Custom Bouquets",
    ),
    st.Page(
        page="pages/checkout.py",
        title="Checkout Page",
    ),
    st.Page(
        page="pages/mycart.py",
        title="My Cart",
    ),
    st.Page(
        page="pages/_shop_detail.py",
        title="Shop",
    ),
]

# ---- CUSTOM SIDEBAR NAVIGATION ----

# Filter out hidden pages (those without icons)
visible_pages = [page for page in pages if page.icon]

# Create custom navigation links
with st.sidebar:
    navigation = st.container(key="nav")
    with navigation:
        for page in visible_pages:
            st.page_link(page, label=f"{page.title}", icon=f"{page.icon}")

    # Add auth section
    auth = st.container(key="auth")
    with auth:
        st.markdown("---")
        st.image(
            "assets/Bouq-it.png",
            use_container_width=True,
        )
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
pg = st.navigation(pages=pages, position="hidden")
pg.run()

# ---- SHARED ON ALL views ----
