import requests
import streamlit as st
from PIL import Image
from sqlalchemy import select

from dependencies.database import *

db: Session = st.session_state["db"]
st.title("Shop Catalogue")

st.header("Shops")


@st.cache_data(show_spinner=False)
def fetch(url: String):
    data = Image.open(requests.get(url, stream=True).raw)
    return data


queryShop = select(Shop.name, Shop.address, Shop.barangay, Shop.city)
all_shops = db.execute(queryShop).all()

shops = st.container(key="shops")

with shops:
    num_shops = len(all_shops)
    num_rows = (num_shops + 3) // 4
    for row in range(num_rows):
        col = st.columns(4, gap="small", border=True)
        for i in range(4):
            shop_index = row * 4 + i
            if shop_index < num_shops:
                name, address, barangay, city = all_shops[shop_index]
                with col[i]:
                    img = fetch("https://picsum.photos/400/500")
                    st.image(img)
                    st.subheader(name)
                    st.write(f"{address}")
                    st.write(f"{barangay}")
                    st.write(f"{city}")

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
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)
