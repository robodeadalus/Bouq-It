import streamlit as st
from sqlalchemy import select

from dependencies.database import *

# Set page title
st.title("Shop Details")

# Check if we have a selected shop
if "selected_shop_id" not in st.session_state:
    st.warning("No shop selected. Redirecting to homepage...")
    st.switch_page("app.py")  # or your main page filename

# Get database session
db: Session = st.session_state["db"]

# Fetch the selected shop details
query = select(Shop).where(Shop.id == st.session_state["selected_shop_id"])
selected_shop = db.execute(query).scalar_one()

# Display shop details
st.header(selected_shop.name)
st.write(f"**Location:** {selected_shop.location}")
st.write(f"**Sales:** {selected_shop.sales}")
st.write(f"**Description:** {selected_shop.description}")

# You can add more details as needed
# For example, if you have products associated with the shop:
st.subheader("Available Products")
products_query = select(ShopFlower).where(ShopFlower.shop_id == selected_shop.id)
products: list[ShopFlower] = db.execute(products_query).scalars().all()

for product in products:
    st.write(product.flower_name)

# Back button
if st.button("Back to Home"):
    st.switch_page("app.py")  # or your main page filename
