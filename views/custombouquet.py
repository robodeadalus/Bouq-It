import pandas as p
import streamlit as st
from PIL import Image
from sqlalchemy import select

from dependencies.database import *

db: Session = st.session_state["db"]
engine = st.session_state["engine"]

if "custom_bouquet" in st.session_state:
    custom_bouquet = st.session_state["custom_bouquet"]
else:
    custom_bouquet = {
        "shop": None,
        "contents": list(),
    }

print(custom_bouquet)


@st.dialog("Add Flowers")
def add_flower(shop: Shop):
    custom_bouquet["shop"] = Shop
    flowers_query = select(ShopFlower).where(ShopFlower.shop_id == selected_shop.id)
    flowers = [f[0] for f in db.execute(flowers_query).all()]
    quantity = st.number_input("Quantity", format="%d", step=1, min_value=1)
    flower = st.selectbox(
        "Flower",
        flowers,
        format_func=lambda a: a.flower_name,
        placeholder="Select Flower",
        label_visibility="collapsed",
    )
    if st.button("Submit"):
        custom_bouquet["shop"] = selected_shop
        contents = []
        custom_bouquet["contents"].append((flower, quantity))
        st.session_state["custom_bouquet"] = custom_bouquet
        st.rerun()
        print(custom_bouquet)


st.title("Custom Bouquet")

query = select(Shop)
shops = map(lambda s: s[0], db.execute(query).all())

selected_shop: Shop = st.selectbox(
    "From Shop:",
    shops,
    format_func=lambda a: a.name,
    placeholder="Select Shop",
    label_visibility="collapsed",
)

if st.button("Add Flower"):
    add_flower(selected_shop)

ordered_flowers = st.container(border=True)

with ordered_flowers:
    if "custom_bouquet" in st.session_state:
        cols = st.columns([0.2, 0.8], gap="small", vertical_alignment="center")
        cols[0].write("Quantity")
        cols[1].write("Flower")
        contents = st.session_state["custom_bouquet"]["contents"]
        for flower, quantity in contents:
            cols[0].write(str(quantity))
            cols[1].write(flower.flower_name)


custom_css = """
<style>
    .stSelectbox div > * {
        color: white !important;
    }
    li[aria-selected="true"] div {
        color: white;
    }
    [data-testid="stNumberInputContainer"] input {
        color: white;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)
