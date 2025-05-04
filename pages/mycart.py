import streamlit as st
from sqlalchemy import select

from dependencies.database import *

if not st.session_state["authentication_status"]:
    print(True)
    st.switch_page("./pages/homepage.py")


if "user_id" not in st.session_state:
    st.warning("Please login to view your cart")
    st.switch_page("./pages/login.py")


db: Session = st.session_state["db"]


if "selected_items" not in st.session_state:
    st.session_state.selected_items = {}

st.title("Your Shopping Cart")


def get_cart_contents(user_id: int):

    flowers = db.execute(
        select(CustomerFlower, Flower)
        .join(Flower, CustomerFlower.flower_name == Flower.name)
        .where(CustomerFlower.customer_id == user_id)
    ).all()

    bouquets = db.execute(
        select(CustomerBouquet, Bouquet)
        .join(Bouquet, CustomerBouquet.bouquet_name == Bouquet.name)
        .where(CustomerBouquet.customer_id == user_id)
    ).all()

    custom_bouquets = (
        db.execute(select(CustomBouquet).where(CustomBouquet.customer_id == user_id))
        .scalars()
        .all()
    )

    return flowers, bouquets, custom_bouquets


flowers, bouquets, custom_bouquets = get_cart_contents(st.session_state.user_id)

# for custom_bouquet in custom_bouquets:
#     print(custom_bouquet[0])
#     # print(custom_bouquet.bouquet_name)

if not flowers and not bouquets and not custom_bouquets:
    st.info("Your cart is empty")
    st.stop()


with st.form("cart_form"):
    st.subheader("Select Items for Checkout")

    for cf, flower in flowers:
        key = f"flower_{flower.name}"
        checked = st.checkbox(
            f"{flower.name} (₱{flower.price:.2f} × {cf.quantity})",
            value=st.session_state.selected_items.get(key, False),
            key=key,
        )
        st.session_state.selected_items[key] = checked

    for cb, bouquet in bouquets:
        key = f"bouquet_{bouquet.name}"
        checked = st.checkbox(
            f"{bouquet.name} (₱{bouquet.price:.2f} × {cb.quantity})"
            + (f" - Design: {cb.design}" if cb.design else ""),
            value=st.session_state.selected_items.get(key, False),
            key=key,
        )
        st.session_state.selected_items[key] = checked

    for custom_bouquet in custom_bouquets:
        key = f"custom_{custom_bouquet.bouquet_name}"
        checked = st.checkbox(
            f"{custom_bouquet.bouquet_name} (₱{custom_bouquet.price:.2f})"
            + (f" - Design: {custom_bouquet.design}" if custom_bouquet.design else ""),
            value=st.session_state.selected_items.get(key, False),
            key=key,
        )
        st.session_state.selected_items[key] = checked

    if st.form_submit_button("Proceed with Selected Items"):

        selected = [k for k, v in st.session_state.selected_items.items() if v]

        if not selected:
            st.warning("Please select at least one item to proceed")
        else:
            st.switch_page("./pages/checkout.py")

st.divider()
if st.button("🔄 Refresh Cart"):
    st.rerun()
