import streamlit as st
from sqlalchemy import join, select

from dependencies.database import *

st.title("Shop Details")

if "selected_shop_id" not in st.session_state:
    st.warning("No shop selected. Redirecting to homepage...")
    st.switch_page("./pages/homepage.py")

db: Session = st.session_state["db"]

flower_query = select(Shop).where(Shop.id == st.session_state["selected_shop_id"])
selected_shop = db.execute(flower_query).scalar_one()

st.header(selected_shop.name)
col1, col2 = st.columns(2)
with col1:
    st.write(f"**Address:** {selected_shop.address}")
    st.write(f"**Barangay:** {selected_shop.barangay}")
    st.write(f"**City:** {selected_shop.city}, {selected_shop.zipcode}")
with col2:
    st.write(f"**Contact No.:** {selected_shop.contact}")
    st.write(f"**Total Sales:** {selected_shop.sales}")

st.divider()

st.subheader("Available Flowers", anchor=False)

flower_query = (
    select(ShopFlower, Flower)
    .join(Flower, ShopFlower.flower_name == Flower.name)
    .where(ShopFlower.shop_id == selected_shop.id)
    .order_by(Flower.name)
)

flower_results = db.execute(flower_query).all()

if not flower_results:
    st.info("This shop currently has no flowers available.")
else:
    for shop_flower, flower in flower_results:
        with st.expander(f"{flower.name} - ₱{flower.price:.2f}"):
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(flower.image_link, use_container_width=True)

            with col2:
                st.write(f"**Price:** ₱{flower.price:.2f}")
                st.write(f"**Available Quantity:** {shop_flower.quantity}")
                st.write(f"**Origin:** {flower.origin}")
                st.write(f"**Meaning:** {flower.meaning}")
                st.write(f"**Description:** {flower.description}")

                if "user_id" not in st.session_state:
                    st.warning("Please login to add items to your cart")
                else:
                    max_qty = min(shop_flower.quantity, 10)
                    qty = st.number_input(
                        "Quantity",
                        min_value=1,
                        max_value=max_qty,
                        value=1,
                        key=f"qty_{flower.name}",
                    )

                    if st.button("Add to Cart", key=f"add_{flower.name}"):
                        try:

                            cart_item = db.execute(
                                select(CustomerFlower)
                                .where(
                                    CustomerFlower.customer_id
                                    == st.session_state.user_id
                                )
                                .where(CustomerFlower.flower_name == flower.name)
                            ).scalar_one_or_none()

                            if cart_item:

                                new_qty = cart_item.quantity + qty
                                if new_qty > shop_flower.quantity:
                                    st.error("Not enough stock for this quantity")
                                else:
                                    cart_item.quantity = new_qty
                                    db.commit()
                            else:

                                new_item = CustomerFlower(
                                    customer_id=st.session_state.user_id,
                                    flower_name=flower.name,
                                    quantity=qty,
                                )
                                db.add(new_item)
                                db.commit()

                        except Exception as e:
                            db.rollback()
                            st.error(f"Error updating cart: {str(e)}")

                        finally:
                            st.toast(f"Added {qty} {flower.name} to cart")

st.subheader("Available Bouquets", anchor=False)

bouquet_query = (
    select(ShopBouquet, Bouquet)
    .join(Bouquet, ShopBouquet.bouquet_name == Bouquet.name)
    .where(ShopBouquet.shop_id == selected_shop.id)
    .order_by(Bouquet.name)
)

bouquet_results = db.execute(bouquet_query).all()

if not bouquet_results:
    st.info("This shop currently has no bouquets available.")
else:
    for shop_bouquet, bouquet in bouquet_results:
        with st.expander(f"{bouquet.name} - ₱{bouquet.price:.2f}"):
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(bouquet.image_link, use_container_width=True)

            with col2:
                st.write(f"**Price:** ₱{bouquet.price:.2f}")
                st.write(f"**Origin:** {bouquet.origin}")
                st.write(f"**Meaning:** {bouquet.meaning}")
                st.write(f"**Description:** {bouquet.description}")

                # Get flowers in bouquet
                flowers_query = select(BouquetFlower).where(
                    BouquetFlower.bouquet_name == bouquet.name
                )
                bouquet_flowers = db.execute(flowers_query).scalars().all()

                if bouquet_flowers:
                    st.write("**Contains:**")
                    for bf in bouquet_flowers:
                        st.write(f"- {bf.flower_name} ({bf.quantity}x)")

                if "user_id" not in st.session_state:
                    st.warning("Please login to add items to your cart")
                else:
                    max_qty = min(shop_bouquet.quantity, 5)  # Lower max for bouquets
                    qty = st.number_input(
                        "Quantity",
                        min_value=1,
                        max_value=max_qty,
                        value=1,
                        key=f"qty_bq_{bouquet.name}",
                    )

                    if st.button("Add to Cart", key=f"add_bq_{bouquet.name}"):
                        try:
                            # Check existing cart item
                            cart_item = db.execute(
                                select(CustomerBouquet)
                                .where(
                                    CustomerBouquet.customer_id
                                    == st.session_state.user_id
                                )
                                .where(CustomerBouquet.bouquet_name == bouquet.name)
                            ).scalar_one_or_none()

                            if cart_item:
                                new_qty = cart_item.quantity + qty
                                if new_qty > shop_bouquet.quantity:
                                    st.error("Not enough stock for this quantity")
                                else:
                                    cart_item.quantity = new_qty
                                    db.commit()
                            else:
                                new_item = CustomerBouquet(
                                    customer_id=st.session_state.user_id,
                                    bouquet_name=bouquet.name,
                                    quantity=qty,
                                )
                                db.add(new_item)
                                db.commit()

                            st.toast(f"Added {qty} {bouquet.name} to cart")

                        except Exception as e:
                            db.rollback()
                            st.error(f"Error updating cart: {str(e)}")
