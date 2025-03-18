import requests
import streamlit as st
from PIL import Image
from sqlalchemy import select

from dependencies.database import *

db: Session = st.session_state["db"]
st.title("Homepage")

search_bar = st.text_input("none", placeholder="Search", label_visibility="hidden")


@st.cache_data(show_spinner=False)
def fetch(url: String):
    data = Image.open(requests.get(url, stream=True).raw)
    return data


st.header("Best-Selling Flower Shops")

queryShop = select(Shop.name, Shop.sales).order_by(Shop.sales.desc()).limit(4)
topFourShops = db.execute(queryShop).all()

bestShop = st.container(
    key="best shop",
)
with bestShop:
    cols = st.columns(
        len(topFourShops), gap="small", border=True
    )  # Adjust for available shops
    i = 0
    for shop, sales in topFourShops:
        with cols[i]:
            img = fetch("https://picsum.photos/400/500")
            st.image(img)  # Replace with actual shop images
            st.subheader(shop)
            st.write(f"Sales: {sales}")
        i += 1


# Best-Selling Flowers
st.header("Best-Selling Flowers")
queryFlowers = (
    select(OrderFlower.flower_name, OrderFlower.quantity)
    .order_by(OrderFlower.quantity.desc())
    .limit(4)
)
topFourFlowers = db.execute(queryFlowers).all()  # Execute query properly

bestFlower = st.container(key="best flower")
with bestFlower:
    cols = st.columns(
        len(topFourFlowers), gap="small", border=True
    )  # Adjust for available data
    i = 0
    for flower, sales in topFourFlowers:
        with cols[i]:
            img = fetch("https://picsum.photos/400/500")
            st.image(img)
            st.subheader(flower)
            st.write(f"Sales: ₱{sales: .2f}")
        i += 1

custom_css = """
<style>
    .st-key-best-shop [data-testid="stColumn"]{
        background-color: white;
    }
    .st-key-best-flower [data-testid="stColumn"] {
        background-color: white;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)
