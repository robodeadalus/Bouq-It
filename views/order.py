import streamlit as st
import requests
from PIL import Image
from sqlalchemy import select
from dependencies.database import *

db: Session = st.session_state["db"]

st.title("Order Page")

search_bar = st.text_input("none", placeholder="Search", label_visibility="hidden")

@st.cache_data
def fetch(url: String):
    data = Image.open(requests.get(url, stream=True).raw)
    return data

query_available_flowers = (
    select(Flower.name, Flower.price)
)

all_available_flowers = db.execute(query_available_flowers).all()

available_flowers = st.container(key="available flowers")

with available_flowers:
    num_flowers = len(all_available_flowers)
    num_rows = (num_flowers + 3) // 4 
    
    for row in range(num_rows):
        cols = st.columns(4, gap="small", border=True)
        
        for col in range(4):
            flower_index = row * 4 + col
        
            if flower_index < num_flowers:
                flower, price = all_available_flowers[flower_index]
                
                with cols[col]:
                    img = fetch("https://picsum.photos/400/500")
                    st.image(img)  # Replace with actual shop images
                    st.subheader(flower)
                    st.write(f"₱{price: .2f}")
                    st.button("", icon=":material/add_circle:", key=f"add_{cols[col]}")

custom_css = """
<style>
    .st-key-available-flowers .stColumn{
        background-color: white;
    }
    .st-key-available-flowers [data-testid="stColumn"] {
        background-color: white;
    }
    .st-key-available-flowers button {
        background-color: white !important;
        margin-top: -50px !important; 
        float: right;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)