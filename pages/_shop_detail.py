import streamlit as st
from sqlalchemy import join, select

from dependencies.database import *

# Set page title
st.title("Shop Details")

# Check if we have a selected shop
if "selected_shop_id" not in st.session_state:
    st.warning("No shop selected. Redirecting to homepage...")
    st.switch_page("./pages/homepage.py")

# Get database session
db: Session = st.session_state["db"]

# Fetch the selected shop details
query = select(Shop).where(Shop.id == st.session_state["selected_shop_id"])
selected_shop = db.execute(query).scalar_one()

# Display shop details
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

# Display available flowers with complete details
st.subheader("Available Flowers")

# Join ShopFlower with Flower to get complete details
query = (
    select(ShopFlower, Flower)
    .join(Flower, ShopFlower.flower_name == Flower.name)
    .where(ShopFlower.shop_id == selected_shop.id)
    .order_by(Flower.name)
)

results = db.execute(query).all()

if not results:
    st.info("This shop currently has no flowers available.")
else:
    for shop_flower, flower in results:
        with st.expander(f"{flower.name} - ₱{flower.price:.2f}"):
            col1, col2 = st.columns([1, 2])
            with col1:
                pass
                # st.image(flower.image_link, width=200)
            with col2:
                st.write(f"**Price:** ₱{flower.price:.2f}")
                st.write(f"**Available Quantity:** {shop_flower.quantity}")
                st.write(f"**Origin:** {flower.origin}")
                st.write(f"**Meaning:** {flower.meaning}")
                st.write(f"**Description:** {flower.description}")
                # You could add an "Add to Cart" button here if needed
