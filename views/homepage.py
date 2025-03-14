import streamlit as st
from sqlalchemy import select
from dependencies.database import *

db = st.connection(
    "postgresql",
    type ="sql",
)
st.session_state["db"]=db
db.session.autoflush=True
st.session_state["db_session"]=db.session
st.title("Homepage")

search_bar = st.text_input("none", placeholder="Search", label_visibility="hidden")


st.header("Best-Selling Flower Shops")

queryShop = select(Shop.name,Shop.sales).order_by(Shop.sales.desc()).limit(4)
topFourShops = db.session.execute(queryShop).fetchall()

shopNames = [shop[0] for shop in topFourShops]  # Get shop names
shopSales = [shop[1] for shop in topFourShops]  # Get sales numbers

bestShop = st.container(key="best shop")
with bestShop:
    cols = st.columns(len(shopNames), gap="small")  # Adjust for available shops
    for i, shop in enumerate(shopNames):  
        with cols[i]:
            st.image("https://picsum.photos/400/500")  # Replace with actual shop images
            st.subheader(shop)
            st.write(f"Sales: {shopSales[i]}")


# Best-Selling Flowers
st.header("Best-Selling Flowers")
queryFlowers = select(OrderFlower.flower_name, OrderFlower.quantity).order_by(OrderFlower.quantity.desc()).limit(4)
topFourFlowers = db.session.execute(queryFlowers).fetchall()  # Execute query properly

# ✅ Extract flower names and sales from query results
flowerNames = [flower[0] for flower in topFourFlowers]  # Get flower names
flowerSales = [flower[1] for flower in topFourFlowers]  # Get corresponding sales

bestFlower = st.container(key="best flower")
with bestFlower:
    cols = st.columns(len(flowerNames), gap="small", border=True)  # Adjust for available data
    for i, flower in enumerate(flowerNames):  
        with cols[i]:
            st.image("https://picsum.photos/400/500")
            st.subheader(flower)
            st.write(f"Sales: {flowerSales[i]}")

custom_css = """
<style>
    .st-key-best-shop .stColumn{
        background-color: white;
    }
    .st-key-best-flower [data-testid="stColumn"] {
        background-color: white;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)
