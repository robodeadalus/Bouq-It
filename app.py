import streamlit as st

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
]

# ---- NAVIGATION SETUP ----
st.sidebar.image(
    "assets/Bouq-it.png",
    use_container_width=True,
)
pg = st.navigation(pages=pages)

with st.sidebar:
    login = st.container(key="login")
    with login:
        st.button("Login", use_container_width=True)

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
    .st-key-login {
        color: white;
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
