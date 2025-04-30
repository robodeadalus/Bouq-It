import requests
import streamlit as st
from PIL import Image
from sqlalchemy import select

from dependencies.database import *
from dependencies.helper import fetch

db: Session = st.session_state["db"]
st.title("Flower Catalogue")


#flowerName = select(Flower.name)
allFlowers = [row[0] for row in db.execute(select(Flower.name)).all()]

# bouquetName = select(Bouquet.name)
allBouquets = [row[0] for row in db.execute(select(Bouquet.name)).all()]

allProducts = allFlowers + allBouquets
selected = st.multiselect("Filter By:", options=allProducts)

if selected:
    queryFlower = select(Flower.name, Flower.short_desc, Flower.image_link).where(Flower.name.in_(selected))
    queryBouquet = select(Bouquet.name, Bouquet.meaning, Bouquet.image_link).where(Bouquet.name.in_(selected))
else:
    queryFlower = select(Flower.name, Flower.short_desc, Flower.image_link).limit(3)
    queryBouquet = select(Bouquet.name, Bouquet.meaning, Bouquet.image_link).limit(3)

topFlowers = db.execute(queryFlower).all()
topBouquets = db.execute(queryBouquet).all()


st.header("Flowers")
flowers = st.container(key="flowers")

@st.dialog("Flower Details")
def show_flower_details(flower_name):
    # Query for the specific flower details
    flower_query = select(Flower).where(Flower.name == flower_name)
    detailed_flower = db.execute(flower_query).scalars().first()
    if detailed_flower:
        st.write(f"**Price:** ₱{detailed_flower.price:.2f}")
        st.write(f"**Origin:** {detailed_flower.origin}")
        st.write(f"**Meaning:** {detailed_flower.meaning}")
        st.write(f"**Description:** {detailed_flower.description}")

@st.dialog("Bouquet Details")
def show_bouquet_details(bouquet_name):
    bouquet_query = select(Bouquet).where(Bouquet.name == bouquet_name)
    detailed_bouquet = db.execute(bouquet_query).scalars().first()
    if detailed_bouquet:
        st.write(f"**Price** ₱{detailed_bouquet.price:.2f}")
        st.write(f"**Origin:** {detailed_bouquet.origin}")
        st.write(f"**Meaning:** {detailed_bouquet.meaning}")
        st.write(f"**Description:** {detailed_bouquet.description}")

with flowers:
    for i in range (0, len(topFlowers), 3):
        batch = topFlowers[i:i+3]
        cols = st.columns(len(batch), gap="small", border = True)
        for j, (flower, desc, image_path) in enumerate(batch): 
            with cols[j]:
                st.image(image_path, use_container_width=True)
                st.subheader(flower)
                st.write(f"{desc}")
                if st.button(f"View", key=f"view_button_flower_{i+j}", use_container_width=True, type="primary"):
                    show_flower_details(flower)

st.header("Bouquets")
bouquets = st.container(key="bouquets")

with bouquets:
    for m in range (0, len(topBouquets), 3):
        batch = topBouquets[m:m+3]
        cols = st.columns(len(batch), gap="small", border = True)
        for n, (bouquet, desc, image_path) in enumerate(batch): 
            with cols[n]:
                st.image(image_path, use_container_width=True)
                st.subheader(bouquet)
                st.write(f"{desc}")
                if st.button(f"View", key=f"view_button_bouquet_{m+n}", use_container_width=True, type= "primary"):
                    show_bouquet_details(bouquet)


custom_css = """
<style>
    div[data-testid="stColumn"] {
        display: block;
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
    img {
    height: 200px;
    width: 100%;
    object-fit: cover;
    border-radius: 10px;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)
