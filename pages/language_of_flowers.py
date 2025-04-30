import streamlit as st
from PIL import Image
from sqlalchemy import select
from st_keyup import st_keyup

from dependencies.database import *
from dependencies.helper import fetch

db: Session = st.session_state["db"]

st.title("Language of Flowers")
#search_bar = st.text_input("none", placeholder="Search", label_visibility="hidden")
search = st_keyup("Search", key="0") #https://pypi.org/project/streamlit-keyup/

query_flowers = (
    select(Flower.name, Flower.description, Flower.short_desc, Flower.origin, Flower.meaning)
)
query_bouquets = (
    select(Bouquet.name, Bouquet.description, Bouquet.short_desc, Bouquet.origin, Bouquet.meaning)
)

all_flowers = db.execute(query_flowers).all()
all_bouquets = db.execute(query_bouquets).all()

if search:
    all_flowers = [
        (name, desc, short_desc, origin, meaning)
        for name, desc, short_desc, origin, meaning in all_flowers
        if search.lower() in name.lower() 
        or search.lower() in desc.lower()
        or search.lower() in short_desc.lower()
        or search.lower() in origin.lower()
        or search.lower() in meaning.lower()
        ]
    all_bouquets = [
        (name, desc, short_desc, origin, meaning)
        for name, desc, short_desc, origin, meaning in all_bouquets
        if search.lower() in name.lower() 
        or search.lower() in desc.lower()
        or search.lower() in short_desc.lower()
        or search.lower() in origin.lower()
        or search.lower() in meaning.lower()
        ]
    #https://discuss.streamlit.io/t/how-to-create-a-search-field-for-the-app/36074/4

st.header("Flowers")
flowers = st.container(key="flowers")

with flowers:
    num_flowers = len(all_flowers)
    num_rows = (num_flowers + 3) // 4
    for row in range(num_rows):
        col = st.columns(4, gap="small", border=True)
        for i in range(4):
            flower_index = row * 4 + i
            if flower_index < num_flowers:
                name, desc, short_desc, origin, meaning = all_flowers[flower_index]
                with col[i]:
                    img = fetch("https://picsum.photos/400/500")
                    st.image(img)
                    st.subheader(name)
                    st.write(f"{meaning}")
                    st.write(f"{desc}")
                    st.write(f"{origin}")

st.header("Bouquets")
bouquets = st.container(key="bouquets")

with bouquets:
    num_bouquets = len(all_bouquets)
    num_rows = (num_bouquets + 3) // 4
    for row in range(num_rows):
        col = st.columns(4, gap="small", border=True)
        for i in range(4):
            flower_index = row * 4 + i
            if flower_index < num_bouquets:
                name, desc, short_desc, origin, meaning = all_bouquets[flower_index]
                with col[i]:
                    img = fetch("https://picsum.photos/400/500")
                    st.image(img)
                    st.subheader(name)
                    st.write(f"{meaning}")
                    st.write(f"{desc}")
                    st.write(f"{origin}")

custom_css = """
<style>
    div[data-testid="stColumn"] {
        display: flex;
    }
    .desc {
        padding: 10px;
        text-align: center;
    }
    .st-key-bouquets .stColumn  {
        background-color: white;
    }
    .st-key-bouquets [data-testid="stHorizontalBlock"] {
        padding: 10px;
        border-radius: 5px;
        transition: background-color 0.3s;
    }

    .st-key-flowers .stColumn  {
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
