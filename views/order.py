import streamlit as st
import requests
from PIL import Image
from sqlalchemy import select
from dependencies.database import *

db: Session = st.session_state["db"]

if "cart" not in st.session_state:
    st.session_state["cart"] = []

st.title("Order Page")
search_bar = st.text_input("none", placeholder="Search", label_visibility="hidden")
st.header("Available Flowers")

def add_to_cart(flower_name, price, shop_name):
    st.session_state["cart"].append({"flower": flower_name, "price": price, "shop": shop_name})
    st.success(f"Added {flower_name} to cart!")

@st.cache_data
def fetch(url: String):
    data = Image.open(requests.get(url, stream=True).raw)
    return data

query_available_flowers = (
    select(
        Flower.name,
        Flower.price,
        Shop.name.label("shop_name")
    )
    .join(ShopFlower, Flower.name == ShopFlower.flower_name)
    .join(Shop, ShopFlower.shop_id == Shop.id)
    .filter(ShopFlower.quantity > 0)
)

all_available_flowers = db.execute(query_available_flowers).all()

available_flowers = st.container(key="available flowers")

with available_flowers:
    if all_available_flowers:
        num_flowers = len(all_available_flowers)
        num_rows = (num_flowers + 3) // 4  
        
        for row in range(num_rows):
            cols_in_this_row = min(4, num_flowers - row * 4)
            
            if cols_in_this_row > 0:
                cols = st.columns(cols_in_this_row, gap="small", border=True)
                
                for col in range(cols_in_this_row):
                    flower_index = row * 4 + col
                    
                    if flower_index < num_flowers:
                        flower, price, shop_name = all_available_flowers[flower_index]
                        
                        with cols[col]:
                            img = fetch("https://picsum.photos/400/500")
                            st.image(img)
                            st.subheader(flower)
                            st.write(shop_name)
                            st.write(f"₱{price:.2f}")
                            
                            if st.button("", icon=":material/add_circle:", key=f"add_{cols[col]}"):
                                add_to_cart(flower, price, shop_name)
            else:
                st.info("No flowers available at the moment.")

st.header("Available Bouquets")

st.header("Shopping Cart")
if st.session_state["cart"]:
    for item in st.session_state["cart"]:
        st.write(f"{item['flower']} - ₱{item['price']:.2f} ({item['shop']})")
else:
    st.write("Your cart is empty.")

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