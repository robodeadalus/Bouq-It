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


@st.dialog("Add Flowers")
def add_flower(shop: Shop):
    custom_bouquet["shop"] = Shop
    flowers_query = select(ShopFlower).where(ShopFlower.shop_id == shop.id)
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

        found = False
        for i, (q, f) in enumerate(custom_bouquet["contents"]):
            if f.flower_name == flower.flower_name:
                custom_bouquet["contents"][i] = (q + quantity, f)
                found = True
                break
        if not found:
            custom_bouquet["contents"].append((quantity, flower))

        st.session_state["custom_bouquet"] = custom_bouquet
        st.rerun()


def validate_shop():
    if "custom_bouquet" not in st.session_state:
        return None

    curr_shop = st.session_state["custom_bouquet"]["shop"]
    sel_shop = st.session_state["shop"]

    if curr_shop is not None and curr_shop.id != sel_shop.id:
        st.session_state["custom_bouquet"] = {
            "shop": sel_shop,
            "contents": [],
        }


st.title("Custom Bouquet")

query = select(Shop)
shops = map(lambda s: s[0], db.execute(query).all())

selected_shop: Shop = st.selectbox(
    "From Shop:",
    shops,
    key="shop",
    format_func=lambda a: a.name,
    placeholder="Select Shop",
    label_visibility="collapsed",
    on_change=validate_shop,
)

if st.button("Add Flower"):
    add_flower(selected_shop)

ordered_flowers = st.container(border=True)

with ordered_flowers:
    if (
        "custom_bouquet" in st.session_state
        and st.session_state["custom_bouquet"]["contents"]
    ):
        contents = [
            (True, q, f.flower_name)
            for q, f in st.session_state["custom_bouquet"]["contents"]
        ]

        df = p.DataFrame(
            contents,
            columns=["", "Quantity", "Flower"],
        )

        column_config = {
            "": st.column_config.CheckboxColumn(
                "",
                width="small",
                default=True,
            ),
            "Quantity": st.column_config.NumberColumn(
                "Quantity",
                width="small",
                disabled=True,
            ),
            "Flower": st.column_config.Column(
                "Flower",
                width="large",
                disabled=True,
            ),
        }

        st.data_editor(df, hide_index=True, column_config=column_config)
        st.button("Add to Cart")
        if st.button("Clear Current Bouquet"):
            st.session_state["custom_bouquet"]["contents"] = []
            st.rerun()
