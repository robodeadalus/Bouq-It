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


def add_to_cart(item_name: str, item_type: str):
    if "user_id" not in st.session_state:
        st.warning("Please login to add items to cart")
        return

    user_id = st.session_state["user_id"]

    try:
        if item_type == "flower":
            existing = db.execute(
                select(CustomerFlower)
                .where(CustomerFlower.customer_id == user_id)
                .where(CustomerFlower.flower_name == item_name)
            ).scalar_one_or_none()

            if existing:
                existing.quantity += 1
                db.commit()
                st.success(f"Added another {item_name} to your cart")
            else:
                cf = CustomerFlower(
                    customer_id=user_id, flower_name=item_name, quantity=1
                )
                db.add(cf)
                db.commit()
                st.success(f"Added {item_name} to your cart")

        elif item_type == "bouquet":
            existing = db.execute(
                select(CustomerBouquet)
                .where(CustomerBouquet.customer_id == user_id)
                .where(CustomerBouquet.bouquet_name == item_name)
            ).scalar_one_or_none()

            if existing:
                existing.quantity += 1
                db.commit()
                st.success(f"Added another {item_name} bouquet to your cart")
            else:
                cb = CustomerBouquet(
                    customer_id=user_id, bouquet_name=item_name, quantity=1
                )
                db.add(cb)
                db.commit()
                st.success(f"Added {item_name} bouquet to your cart")

    except SQLAlchemyError as e:
        db.rollback()
        st.error(f"Database error: {e}")


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
