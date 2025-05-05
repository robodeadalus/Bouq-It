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

st.subheader("Shipping Details", anchor=False)
col1, col2 = st.columns(2)
with col1:
    st.write(f"**Name:** {user.first_name} {user.last_name}")
    st.write(f"**Address:** {user.address}")
with col2:
    st.write(f"**Barangay:** {user.barangay}")
    st.write(f"**City:** {user.city}, {user.zipcode}")
    st.write(f"**Contact:** {user.contact}")

st.divider()

st.subheader("Order Summary", anchor=False)
total = 0

if "flowers" in st.session_state["checkout"] and st.session_state["checkout"]["flowers"]:
    st.write("**Flowers**")
    for cf, flower in st.session_state["checkout"]["flowers"]:
        item_total = flower.price * cf.quantity
        total += item_total
        st.write(f"- {flower.name}")
        st.write(f"  Quantity: {cf.quantity}")
        st.write(f"  Price: ₱{flower.price:.2f} × {cf.quantity} = ₱{item_total:.2f}")

if "bouquets" in st.session_state["checkout"] and st.session_state["checkout"]["bouquets"]:
    st.write("**Pre-made Bouquets**")
    for cb, bouquet in st.session_state["checkout"]["bouquets"]:
        item_total = bouquet.price * cb.quantity
        total += item_total
        st.write(f"- {bouquet.name}")
        st.write(f"  Quantity: {cb.quantity}")
        if cb.design:
            st.write(f"  Design: {cb.design}")
        st.write(f"  Price: ₱{bouquet.price:.2f} × {cb.quantity} = ₱{item_total:.2f}")

if "custom" in st.session_state["checkout"] and st.session_state["checkout"]["custom"]:
    st.write("**Custom Bouquets**")
    for cb in st.session_state["checkout"]["custom"]:
        total += cb.price
        st.write(f"- {cb.bouquet_name}")
        if cb.design:
            st.write(f"  Design: {cb.design}")
        st.write(f"  Price: ₱{cb.price:.2f}")

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
                    cb: CustomBouquet
                    design_items = cb.design.split("\n")
                    for item in design_items:
                        if "x" in item:
                            quantity, flower_name = item.split("x")
                            quantity = int(quantity.strip().split(" ")[0])
                            flower_name = flower_name.split("@")[0].strip()

                            shop_flower = db.execute(
                                select(ShopFlower)
                                .where(ShopFlower.shop_id == cb.shop_id)
                                .where(ShopFlower.flower_name == flower_name)
                            ).scalar_one()

                            shop_flower.quantity -= quantity
                            db.add(shop_flower)

                    db.execute(
                        insert(OrderCustom).values(
                            order_id=new_order.id,
                            custom_bouquet_id=cb.bouquet_name,
                        )
                    )

                    db.delete(cb)

            db.commit()
            st.success("Order placed successfully! 🎉")

            st.session_state["checkout"] = {}
            st.session_state.selected_items = {}
            st.switch_page("pages/myorders.py")

        except SQLAlchemyError as e:
            db.rollback()
            st.error(f"Error processing order: {str(e)}")

st.divider()
if st.button("← Return to Cart"):
    st.switch_page("./pages/mycart.py")
