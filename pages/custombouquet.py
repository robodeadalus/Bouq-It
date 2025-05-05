import pandas as p
import streamlit as st
from PIL import Image
from sqlalchemy import select

from dependencies.database import *

db: Session = st.session_state["db"]
engine = st.session_state["engine"]

if "custom_bouquet" in st.session_state:
    custom_bouquet = st.session_state["custom_bouquet"]
else:
    custom_bouquet = {
        "shop": None,
        "contents": list(),
    }


@st.dialog("Add Flowers")
def add_flower(shop: Shop):

    custom_bouquet["shop"] = shop

    flowers_query = (
        select(ShopFlower, Flower)
        .join(Flower, ShopFlower.flower_name == Flower.name)
        .where(ShopFlower.shop_id == shop.id)
    )

    results = db.execute(flowers_query).all()

    available_flowers = [(sf, flower) for sf, flower in results]

    # Display flower selector with prices

    flower_options = {
        f"{flower.name} (₱{flower.price:.2f})": (sf, flower)
        for sf, flower in available_flowers
    }

    selected = st.selectbox(
        "Select Flower",
        options=list(flower_options.keys()),
        format_func=lambda x: x,
        placeholder="Select Flower",
    )

    quantity = st.number_input(
        "Quantity",
        min_value=1,
        max_value=flower_options[selected][0].quantity,  # Use shop quantity
        value=1,
    )

    if st.button("Add Flower", key="add_flower"):
        flower: Flower = flower_options[selected][1]

        # Check if flower already in bouquet
        found = False
        for i, (f, q) in enumerate(custom_bouquet["contents"]):
            if f.name == flower.name:
                custom_bouquet["contents"][i] = (f, q + quantity)
                found = True
                break

        if not found:
            custom_bouquet["contents"].append((flower, quantity))

        st.session_state.custom_bouquet = custom_bouquet
        st.rerun()


def validate_shop():
    if "custom_bouquet" not in st.session_state:
        return None

    curr_shop = st.session_state["custom_bouquet"]["shop"]
    sel_shop = st.session_state["shop"]

    if curr_shop is not None and curr_shop.id != sel_shop.id:
        st.session_state["custom_bouquet"] = {
            "shop": sel_shop,
            "contents": [],
        }


st.title("Custom Bouquet")

query = select(Shop)
shops = map(lambda s: s[0], db.execute(query).all())

selected_shop: Shop = st.selectbox(
    "From Shop:",
    shops,
    key="shop",
    format_func=lambda a: a.name,
    placeholder="Select Shop",
    label_visibility="collapsed",
    on_change=validate_shop,
)

if st.button("Add Flower"):
    add_flower(selected_shop)

ordered_flowers = st.container(border=True)

with ordered_flowers:
    if (
        "custom_bouquet" in st.session_state
        and st.session_state["custom_bouquet"]["contents"]
    ):
        contents = [
            (True, q, f.name, float(f.price) * q)
            for f, q in st.session_state["custom_bouquet"]["contents"]
        ]

        df = p.DataFrame(
            contents,
            columns=["", "Quantity", "Flower", "Price"],
        )

        column_config = {
            "": st.column_config.CheckboxColumn(
                "",
                width="small",
                default=True,
            ),
            "Quantity": st.column_config.NumberColumn(
                "Quantity",
                width="small",
                disabled=True,
            ),
            "Flower": st.column_config.Column(
                "Flower",
                width="medium",
                disabled=True,
            ),
            "Price": st.column_config.NumberColumn(
                "Price",
                width="medium",
                format="PHP %.2f",
                disabled=True,
            ),
        }

        edited_df = st.data_editor(df, hide_index=True, column_config=column_config)

        selected_rows = edited_df[edited_df[""]].index.tolist()

        st.session_state["custom_bouquet"]["contents"] = [
            item
            for idx, item in enumerate(st.session_state["custom_bouquet"]["contents"])
            if idx in selected_rows
        ]

        if st.button("Clear Current Bouquet"):
            st.session_state["custom_bouquet"]["contents"] = []
            st.rerun()

        if "user_id" in st.session_state:
            if st.button("Add to Cart"):
                custom_bouquet = st.session_state["custom_bouquet"]
                selected_shop = custom_bouquet["shop"]

                if not custom_bouquet["contents"]:
                    st.error("Please add flowers to your bouquet first")
                    st.stop()

                # Calculate total price
                total_price = sum(f.price * q for f, q in custom_bouquet["contents"])

                # Create design description
                design_desc = "\n".join(
                    f"{q}x {f.name} @ PHP {f.price:.2f}"
                    for f, q in custom_bouquet["contents"]
                )

                # Create bouquet record
                new_bouquet = CustomBouquet(
                    customer_id=st.session_state.user_id,
                    bouquet_name="Custom Bouquet",
                    design=f"Custom Bouquet from {selected_shop.name}\n{design_desc}",
                    price=total_price,
                )

                db.add(new_bouquet)
                db.commit()

                st.success(f"Custom bouquet (₱{total_price:.2f}) added to cart!")
                st.session_state.custom_bouquet = {"shop": None, "contents": []}
                st.rerun()
