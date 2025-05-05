import math

import requests
import streamlit as st
from PIL import Image
from sqlalchemy import select

from dependencies.database import *
from dependencies.helper import fetch

db: Session = st.session_state["db"]
st.title("Shop Catalogue")

st.header("Shops")

queryShop = select(Shop).order_by(Shop.name)
all_shops = db.execute(queryShop).scalars().all()


shops = st.container(key="shops")

with shops:
    total_shops = len(all_shops)
    num_rows = math.ceil(total_shops / 3)

    for row in range(num_rows):
        cols = st.columns(3, gap="small", border=True)
        for i, col in enumerate(cols):
            shop_index = row * 3 + i
            if shop_index < total_shops:
                shop = all_shops[shop_index]
                with col:
                    st.image(shop.image_link, use_container_width=True)
                    st.subheader(shop.name, anchor=False)
                    st.write(shop.address)
                    st.write(shop.barangay)
                    st.write(shop.city)
                    if st.button(
                        "View",
                        key=f"shop_{shop.id}",
                        use_container_width=True,
                        type="primary",
                    ):
                        st.session_state["selected_shop_id"] = shop.id
                        st.switch_page("pages/_shop_detail.py")
            else:
                with col:
                    st.write("")

custom_css = """
<style>
    div[data-testid="stColumn"] {
        display: flex;
    }
    .desc {
        padding: 10px;
        text-align: center;
    }
    .st-key-shops .stColumn  {
        background-color: white;
    }
    .st-key-shops [data-testid="stHorizontalBlock"] {
        padding: 10px;
        border-radius: 5px;
        transition: background-color 0.3s;
    }
    h3 {
        height: 5.5rem;
        overflow: hidden;
        white-space: pre-wrap;
        text-overflow: ellipsis;
        word-break: initial;
    }
    img {
    height: 200px;
    width: 100%;
    object-fit: cover;
    border-radius: 10px;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)
