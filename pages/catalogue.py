import requests
import streamlit as st
from PIL import Image
from sqlalchemy import select

from dependencies.database import *
from dependencies.helper import fetch

db: Session = st.session_state["db"]
st.title("Flower Catalogue")

queryFlower = select(Flower.name, Flower.short_desc).limit(3)
topFlowers = db.execute(queryFlower).all()

flowerName = select(Flower.name)
allFlowers = [row[0] for row in db.execute(flowerName).all()]


queryBouquet = select(Bouquet.name, Bouquet.meaning).limit(3)
topBouquets = db.execute(queryBouquet).all()

bouquetName = select(Bouquet.name)
allBouquets = [row[0] for row in db.execute(bouquetName).all()]

allProducts = allFlowers + allBouquets

filter = st.multiselect("Filter By:", options=allProducts)


st.header("Flowers")
flowers = st.container(key="flowers")

with flowers:
    col = st.columns(3, gap="small", border=True)
    i = 0
    for flower, desc in topFlowers:
        with col[i]:
            img = fetch("https://picsum.photos/400/500")
            st.image(img)
            st.subheader(flower)
            st.write(f"{desc}")
        i += 1


st.header("Bouquets")
bouquets = st.container(key="bouquets")

with bouquets:
    col = st.columns(3, gap="small", border=True)
    i = 0
    for name, meaning in topBouquets:
        with col[i]:
            img = fetch("https://picsum.photos/400/500")
            st.image(img)
            st.subheader(name)
            st.write(f"{meaning}")
        i += 1

custom_css = """
<style>
    div[data-testid="stColumn"] {
        display: flex;
    }
    .desc {
        padding: 10px;
        text-align: center;
    }
    .st-key-flowers .stColumn  {
        background-color: white;
    }
    .st-key-bouquets .stColumn {
        background-color: white;
    }
    .st-key-flowers [data-testid="stHorizontalBlock"] {
        padding: 10px;
        border-radius: 5px;
        transition: background-color 0.3s;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)
