import streamlit as st
from sqlalchemy import select

from dependencies.database import *

if "user_id" not in st.session_state:
    st.warning("Please login to checkout")
    st.switch_page("./pages/homepage.py")

if not st.session_state.get("selected_items"):
    st.warning("No items selected for checkout")
    st.switch_page("./pages/cart.py")


db = st.session_state["db"]

st.title("Checkout Summary")


user = db.execute(select(User).where(User.id == st.session_state.user_id)).scalar_one()


st.subheader("Shipping Details")
st.write(f"**Name:** {user.first_name} {user.last_name}")
st.write(f"**Address:** {user.address}")
st.write(f"**Barangay:** {user.barangay}")
st.write(f"**City:** {user.city}, {user.zipcode}")
st.write(f"**Contact:** {user.contact}")

st.divider()


st.subheader("Order Summary")
total = 0


for item_key in st.session_state.selected_items:
    if not st.session_state.selected_items[item_key]:
        continue

    item_type, name = item_key.split("_", 1)

    if item_type == "flower":

        cf = db.execute(
            select(CustomerFlower)
            .where(CustomerFlower.customer_id == st.session_state.user_id)
            .where(CustomerFlower.flower_name == name)
        ).scalar_one()

        flower = db.execute(select(Flower).where(Flower.name == name)).scalar_one()

        st.write(f"🌹 **{name}**")
        st.write(f"Quantity: {cf.quantity}")
        st.write(
            f"Price: ₱{flower.price:.2f} × {cf.quantity} = ₱{flower.price * cf.quantity:.2f}"
        )
        total += flower.price * cf.quantity

    elif item_type == "bouquet":

        cb = db.execute(
            select(CustomerBouquet)
            .where(CustomerBouquet.customer_id == st.session_state.user_id)
            .where(CustomerBouquet.bouquet_name == name)
        ).scalar_one()

        bouquet = db.execute(select(Bouquet).where(Bouquet.name == name)).scalar_one()

        st.write(f"💐 **{name}**")
        st.write(f"Quantity: {cb.quantity}")
        if cb.design:
            st.write(f"Custom Design: {cb.design}")
        st.write(
            f"Price: ₱{bouquet.price:.2f} × {cb.quantity} = ₱{bouquet.price * cb.quantity:.2f}"
        )
        total += bouquet.price * cb.quantity

st.divider()
st.subheader(f"Total: ₱{total:.2f}")


with st.form("checkout_form"):
    st.selectbox(
        "Payment Method",
        ["G-Cash", "Maya", "Cash on Delivery", "Credit/Debit Card"],
        index=0,
    )

    if st.form_submit_button("Confirm Order"):

        st.success("Order placed successfully!")
        st.balloons()
        st.session_state.selected_items = {}
        st.switch_page("./pages/homepage.py")
