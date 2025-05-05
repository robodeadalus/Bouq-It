import streamlit as st
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from dependencies.database import *
from dependencies.helper import fetch

db: Session = st.session_state["db"]

if "cart" not in st.session_state:
    st.session_state["cart"] = []

st.title("Order Page")
search_bar = st.text_input("none", placeholder="Search", label_visibility="hidden")


def add_to_cart(flower_name: str, price: float, shop_name: str):
    db = st.session_state["db"]
    
    # Get the current user ID from session
    if "user_id" not in st.session_state:
        st.error("Please login first!")
        return
    
    user_id = st.session_state["user_id"]
    
    try:
        # Get shop ID from shop name
        shop = db.execute(select(Shop).where(Shop.name == shop_name)).scalar_one()
        
        # Create a new order
        new_order = Order(
            payment="Cash on Delivery",  # Default, can be changed later
            address="",  # Will use customer's address
            barangay="",
            city="",
            zipcode="",
            ordered_by=user_id
        )
        db.add(new_order)
        db.commit()
        
        # Add flower to order_flowers
        order_flower = OrderFlower(
            order_id=new_order.id,
            flower_name=flower_name,
            quantity=1  # Default quantity
        )
        db.add(order_flower)
        
        # Update shop inventory
        shop_flower = db.execute(
            select(ShopFlower)
            .where(ShopFlower.shop_id == shop.id)
            .where(ShopFlower.flower_name == flower_name)
        ).scalar_one()
        shop_flower.quantity -= 1
        
        # Update customer's flower purchases
        customer_flower = db.execute(
            select(CustomerFlower)
            .where(CustomerFlower.customer_id == user_id)
            .where(CustomerFlower.flower_name == flower_name)
        ).scalar_one_or_none()
        
        if customer_flower:
            customer_flower.quantity += 1
        else:
            new_customer_flower = CustomerFlower(
                customer_id=user_id,
                flower_name=flower_name,
                quantity=1
            )
            db.add(new_customer_flower)
        
        db.commit()
        st.success(f"Added {flower_name} to your order!")
        
    except Exception as e:
        db.rollback()
        st.error(f"Failed to add to cart: {str(e)}")

query_available_flowers = (
    select(Flower, ShopFlower, Shop)
    .join(ShopFlower, Flower.name == ShopFlower.flower_name)
    .join(Shop, ShopFlower.shop_id == Shop.id)
    .filter(ShopFlower.quantity > 0)
)

query_available_bouquets = (
    select(Bouquet, ShopBouquet, Shop)
    .join(ShopBouquet, Bouquet.name == ShopBouquet.bouquet_name)
    .join(Shop, ShopBouquet.shop_id == Shop.id)
    .filter(ShopBouquet.quantity > 0)
)

all_available_flowers = db.execute(query_available_flowers).all()
all_available_bouquets = db.execute(query_available_bouquets).all()

st.header("Available Flowers")
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
                        f, fs, s = all_available_flowers[flower_index]

                        with cols[col]:
                            st.image(f.image_link, use_container_width=True)
                            st.subheader(f.name, anchor=False)
                            st.write("*" + s.name + "*")
                            st.write(f"Available: {fs.quantity}")
                            st.write(f"₱{f.price:.2f}")
                            if "user_id" in st.session_state:
                                if st.button(
                                    "",
                                    icon=":material/add_circle:",
                                    key=f"add_{cols[col]}",
                                ):
                                    add_to_cart(f.name, "flower")
            else:
                st.info("No flowers available at the moment.")

st.header("Available Bouquets")
available_bouquets = st.container(key="available bouquets")

with available_bouquets:
    if all_available_bouquets:
        num_bouquets = len(all_available_bouquets)
        num_rows = (num_bouquets + 3) // 4

        for row in range(num_rows):
            cols_in_this_row = min(4, num_bouquets - row * 4)

            if cols_in_this_row > 0:
                cols = st.columns(cols_in_this_row, gap="small", border=True)

                for col in range(cols_in_this_row):
                    bouquet_index = row * 4 + col

                    if bouquet_index < num_bouquets:
                        b, bs, s = all_available_bouquets[bouquet_index]

                        with cols[col]:
                            st.image(b.image_link, use_container_width=True)
                            st.subheader(b.name, anchor=False)
                            st.write("*" + s.name + "*")
                            st.write(f"Available: {bs.quantity}")
                            st.write(f"₱{b.price:.2f}")
                            if "user_id" in st.session_state:
                                if st.button(
                                    "",
                                    icon=":material/add_circle:",
                                    key=f"add_{cols[col]}",
                                ):
                                    add_to_cart(b.name, "bouquet")
            else:
                st.info("No bouquets available at the moment.")

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
    .st-key-available-bouquets .stColumn{
        background-color: white;
    }
    .st-key-available-bouquets [data-testid="stColumn"] {
        background-color: white;
    }
    .st-key-available-bouquets button {
        background-color: white !important;
        margin-top: -50px !important; 
        float: right;
    }
    img {
    height: 200px;
    width: 100%;
    object-fit: cover;
    border-radius: 10px;
    object-position: 20% 1;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)
