import pandas as p
import streamlit as st
from PIL import Image
from sqlalchemy import select

from dependencies.database import *

db: Session = st.session_state["db"]
engine = st.session_state["engine"]

st.title("Custom Bouquet")

query = select(Shop)
shops = map(lambda s: s[0], db.execute(query).all())

selected_shop: Shop = st.selectbox(
    "From Shop:",
    shops,
    format_func=lambda a: a.name,
    key="selectbox",
    placeholder="Select Shop",
    label_visibility="collapsed",
)

try:
    table = select(ShopFlower.flower_name).where(ShopFlower.shop_id == selected_shop.id)
    print(table)
    dataframe = p.read_sql(table, engine)
    st.table(dataframe)
except:
    pass

custom_css = """
<style>
    .st-key-selectbox .stSelectbox div > *{
        color: white !important;
    }
    [data-testid="stSelectboxVirtualDropdown"] li[aria-selected="true"] {
        color: white;
    }
</style>
"""
