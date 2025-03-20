import streamlit as st
import requests
from PIL import Image
from sqlalchemy import select

from dependencies.database import *

db: Session = st.session_state["db"]
st.title("Flower Catalogue")

st.header("Flowers")

@st.cache_data(show_spinner=False)
def fetch(url: String):
    data = Image.open(requests.get(url, stream=True).raw)
    return data

queryFlower = select(Flower.name, Flower.short_desc).limit(4)
topFlowers = db.execute(queryFlower).all()

flowers = st.container(key = "flowers")

with flowers:
    col = st.columns(4, gap="small", border=True)
    i = 0
    for flower, desc in topFlowers:
        with col[i]:
            img = fetch("https://picsum.photos/400/500")
            st.image(img)
            st.subheader(flower)
            st.write(f"{desc}")
        i += 1

st.header("Bouquets")

queryBouquet = select(Bouquet.name, Bouquet.meaning).limit(4)
topBouquets = db.execute(queryBouquet).all()

bouquets = st.container(key = "bouquets")

with bouquets:
    col = st.columns(4, gap="small", border = True)
    i=0
    for bouquet, meaning in topBouquets:
        with col[i]:
            img = fetch("https://picsum.photos/400/500")
            st.image(img)
            st.subheader(bouquet)
            st.write(f"{meaning}")
        i += 1

custom_css = """
<style>
    div[data-testid="stColumn"] {
        display: flex;
        color: green
    }
    .dropdown {
        position: relative;
        display: inline-block;
    }
    .dropdown-content {
        display: none;
        position: absolute;
        background-color: white;
        max-width: 200px;
        z-index: 1;
    }
    .dropdown:hover .dropdown-content {
        display: block;
    }
    .desc {
        padding: 10px;
        text-align: center;
    }
    .st-key-flowers .stColumn  {
        background-color: white;
    }
    .st-key-flowers [data-testid="stHorizontalBlock"] {
        padding: 10px;
        border-radius: 5px;
        transition: background-color 0.3s;
    }
    
    .hover-column:hover {
        background-color: rgba(0, 0, 0, 0.05);
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)