import pandas as pd
import streamlit as st
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import SQLAlchemyError

from dependencies.database import *

if not st.session_state.get("authentication_status", False):
    st.switch_page("./pages/homepage.py")

if "user_id" not in st.session_state or "checkout" not in st.session_state:
    st.warning("No items selected for checkout")
    st.switch_page("./pages/mycart.py")

db: Session = st.session_state["db"]

st.title("Checkout Summary")

user = db.execute(select(User).where(User.id == st.session_state.user_id)).scalar_one()

# Shipping details
st.subheader("Shipping Details", anchor=False)
st.write(f"**Name:** {user.first_name} {user.last_name}")
st.write(f"**Address:** {user.address}")
st.write(f"**Barangay:** {user.barangay}")
st.write(f"**City:** {user.city}, {user.zipcode}")
st.write(f"**Contact:** {user.contact}")

st.divider()

# Build DataFrame for order summary
records = []
total = 0.0

if "flowers" in st.session_state["checkout"]:
    for cf, flower in st.session_state["checkout"]["flowers"]:
        item_total = flower.price * cf.quantity
        total += float(item_total)
        records.append(
            {
                "Type": "Flower",
                "Name": flower.name,
                "Quantity": cf.quantity,
                "Unit Price": float(flower.price),
                "Total": item_total,
            }
        )

if "bouquets" in st.session_state["checkout"]:
    for cb, bouquet in st.session_state["checkout"]["bouquets"]:
        item_total = bouquet.price * cb.quantity
        total += float(item_total)
        name = bouquet.name + (f" ({cb.design})" if cb.design else "")
        records.append(
            {
                "Type": "Bouquet",
                "Name": name,
                "Quantity": cb.quantity,
                "Unit Price": float(bouquet.price),
                "Total": item_total,
            }
        )

if "custom" in st.session_state["checkout"]:
    for cb in st.session_state["checkout"]["custom"]:
        item_total = cb.price
        total += float(item_total)
        name = cb.bouquet_name + (f" ({cb.design})" if cb.design else "")
        records.append(
            {
                "Type": "Custom Bouquet",
                "Name": cb.design.split("\n")[0],
                "Quantity": 1,
                "Unit Price": float(cb.price),
                "Total": item_total,
            }
        )

if records:
    df_summary = pd.DataFrame(records)
    # format currency
    df_summary["Unit Price"] = df_summary["Unit Price"].map(lambda v: f"₱{v:.2f}")
    df_summary["Total"] = df_summary["Total"].map(lambda v: f"₱{v:.2f}")
    st.subheader("Order Summary", anchor=False)
    st.dataframe(df_summary, use_container_width=True, hide_index=True)
else:
    st.info("No items to checkout.")

st.divider()
st.subheader(f"Total: ₱{total:.2f}")

with st.form("checkout_form"):
    payment_method = st.selectbox(
        "Payment Method", ["G-Cash", "Maya", "Cash on Delivery", "Credit/Debit Card"]
    )

    if st.form_submit_button("Confirm Order"):
        try:
            new_order = Order(
                payment=payment_method,
                address=user.address,
                barangay=user.barangay,
                city=user.city,
                zipcode=user.zipcode,
                ordered_by=st.session_state.user_id,
            )
            db.add(new_order)
            db.flush()

            # insert order items and remove from customer tables
            if "flowers" in st.session_state["checkout"]:
                for cf, flower in st.session_state["checkout"]["flowers"]:
                    db.execute(
                        insert(OrderFlower).values(
                            order_id=new_order.id,
                            flower_name=flower.name,
                            quantity=cf.quantity,
                        )
                    )
                    db.delete(cf)

            if "bouquets" in st.session_state["checkout"]:
                for cb, bouquet in st.session_state["checkout"]["bouquets"]:
                    db.execute(
                        insert(OrderBouquet).values(
                            order_id=new_order.id,
                            bouquet_name=bouquet.name,
                            quantity=cb.quantity,
                            design=cb.design,
                        )
                    )
                    db.delete(cb)

            if "custom" in st.session_state["checkout"]:
                for cb in st.session_state["checkout"]["custom"]:
                    db.execute(
                        insert(OrderCustom).values(
                            order_id=new_order.id,
                            custom_bouquet=cb.bouquet_name,
                        )
                    )
                    db.delete(cb)

            db.commit()
            st.success("Order placed successfully! 🎉")

            # Clear state and redirect
            st.session_state["checkout"] = {}
            st.session_state["selected_items"] = {}
            st.switch_page("pages/myorders.py")

        except SQLAlchemyError as e:
            db.rollback()
            st.error(f"Error processing order: {e}")

st.divider()
if st.button("← Return to Cart"):
    st.switch_page("./pages/mycart.py")
