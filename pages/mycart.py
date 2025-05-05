import pandas as pd
import streamlit as st
from sqlalchemy import select

from dependencies.database import *

if not st.session_state["authentication_status"]:
    print(True)
    st.switch_page("./pages/homepage.py")


if "user_id" not in st.session_state:
    st.warning("Please login to view your cart")
    st.switch_page("./pages/login.py")

if "checkout" not in st.session_state:
    st.session_state["checkout"] = dict()


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


def create_category_df(items, item_type):
    data = []
    for idx, item in enumerate(items):
        if item_type == "flower":
            cf, flower = item
            data.append(
                {
                    "Selected": False,
                    "Name": flower.name,
                    "Price": flower.price,
                    "Quantity": cf.quantity,
                    "Total": flower.price * cf.quantity,
                    "Type": "flower",
                    "Index": idx,
                }
            )
        elif item_type == "bouquet":
            cb, bouquet = item
            data.append(
                {
                    "Selected": False,
                    "Name": bouquet.name,
                    "Price": bouquet.price,
                    "Quantity": cb.quantity,
                    "Total": bouquet.price * cb.quantity,
                    "Type": "bouquet",
                    "Index": idx,
                }
            )
        elif item_type == "custom":
            cb = item
            data.append(
                {
                    "Selected": False,
                    "Name": cb.bouquet_name,
                    "Price": cb.price,
                    "Quantity": 1,
                    "Total": cb.price,
                    "Type": "custom",
                    "Index": idx,
                }
            )
    return pd.DataFrame(data)


column_config = {
    "Selected": st.column_config.CheckboxColumn(
        "Select",
        help="Select items to checkout",
        default=False,
        width="small",
    ),
    "Name": st.column_config.TextColumn("Item Name"),
    "Price": st.column_config.NumberColumn(
        "Unit Price",
        format="₱%.2f",
        disabled=True,
        width="small",
    ),
    "Quantity": st.column_config.NumberColumn(
        "Qty",
        disabled=True,
        width="small",
    ),
    "Total": st.column_config.NumberColumn(
        "Total",
        format="₱%.2f",
        disabled=True,
    ),
    "Type": None,
    "Index": None,
}

flowers, bouquets, custom_bouquets = get_cart_contents(st.session_state.user_id)

if not flowers and not bouquets and not custom_bouquets:
    st.info("Your cart is empty")
    st.stop()

cart_contents = st.container()
with cart_contents:

    st.subheader("Your Cart Items", anchor=False)

    edited_flowers = pd.DataFrame()
    edited_bouquets = pd.DataFrame()
    edited_custom = pd.DataFrame()


    if flowers:
        st.write("**Flowers**")
        flowers_df = create_category_df(flowers, "flower")
        edited_flowers = st.data_editor(
            flowers_df,
            column_config=column_config,
            hide_index=True,
            use_container_width=True,
            key="flower_df",
        )

    if bouquets:
        st.write("**Pre-made Bouquets**")
        bouquets_df = create_category_df(bouquets, "bouquet")
        edited_bouquets = st.data_editor(
            bouquets_df,
            column_config=column_config,
            hide_index=True,
            use_container_width=True,
        )

    if custom_bouquets:
        st.write("**Custom Bouquets**")
        custom_df = create_category_df(custom_bouquets, "custom")
        edited_custom = st.data_editor(
            custom_df,
            column_config=column_config,
            hide_index=True,
            use_container_width=True,
        )

    if not edited_flowers.empty:
        selected_flowers = edited_flowers[edited_flowers["Selected"]].index.tolist()
        st.session_state["checkout"]["flowers"] = [
            flower for idx, flower in enumerate(flowers) if idx in selected_flowers
        ]

    if not edited_bouquets.empty:
        selected_bouquets = edited_bouquets[edited_bouquets["Selected"]].index.tolist()
        st.session_state["checkout"]["bouquets"] = [
            bouquet for idx, bouquet in enumerate(bouquets) if idx in selected_bouquets
        ]

    if not edited_custom.empty:
        selected_custom = edited_custom[edited_custom["Selected"]].index.tolist()
        st.session_state["checkout"]["custom"] = [
            custom
            for idx, custom in enumerate(custom_bouquets)
            if idx in selected_custom
        ]


with st.form("cart_form"):

    total = 0

    for category, item in st.session_state["checkout"].items():
        if category == "flowers":
            for i in item:
                total += i[1].price
        if category == "bouquets":
            for i in item:
                total += i[1].price
        if category == "custom":
            for i in item:
                total += i.price

    st.metric("Total Selected Items", value=f"₱{total}")

    if st.form_submit_button("Proceed to Checkout"):
        # Collect selected items
        selected_items = []

        if flowers:
            selected_flowers = edited_flowers[edited_flowers["Selected"]]
            for _, row in selected_flowers.iterrows():
                selected_items.append({"type": "flower", "index": row["Index"]})

        if bouquets:
            selected_bouquets = edited_bouquets[edited_bouquets["Selected"]]
            for _, row in selected_bouquets.iterrows():
                selected_items.append({"type": "bouquet", "index": row["Index"]})

        if custom_bouquets:
            selected_custom = edited_custom[edited_custom["Selected"]]
            for _, row in selected_custom.iterrows():
                selected_items.append({"type": "custom", "index": row["Index"]})

        if not selected_items:
            st.warning("Please select at least one item to proceed")
        else:
            st.session_state.selected_items = selected_items
            st.switch_page("./pages/checkout.py")

st.divider()
if st.button("🔄 Refresh Cart"):
    st.rerun()
