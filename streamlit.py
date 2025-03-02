import streamlit as st

# ---- PAGE SETUP ----
homepage = st.Page(
    page = "views/homepage.py",
    title = "Home Page", 
    icon = ":material/home:",
    default = True
)
catalogue_page = st.Page(
    page = "views/catalogue.py",
    title = "Flower Catalogue", 
    icon = ":material/local_florist:",
)
locator_page = st.Page(
    page = "views/locator.py",
    title = "Flower Shop Locator", 
    icon = ":material/pin_drop:",
)
order_page = st.Page(
    page = "views/order.py",
    title = "Order Page", 
    icon = ":material/shopping_cart:",
)
language_of_flowers_page = st.Page(
    page = "views/language_of_flowers.py",
    title = "Language of Flowers", 
    icon = ":material/auto_stories:",
)

# ---- NAVIGATION SETUP ----
st.sidebar.image("assets/Bouq-it.png", use_container_width = True)
pg =  st.navigation(pages=[homepage,catalogue_page,locator_page,order_page,language_of_flowers_page])

# ---- RUN NAVIGATION ----
pg.run()

# ---- SHARED ON ALL views ----
