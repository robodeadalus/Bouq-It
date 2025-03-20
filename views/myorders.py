import requests
import streamlit as st
from PIL import Image
from sqlalchemy import select

from dependencies.database import *

db: Session = st.session_state["db"]
st.title("My Orders")

search_bar = st.text_input("none", placeholder="Search", label_visibility="hidden")

@st.cache_data(show_spinner=False)
def fetch(url: String):
    data = Image.open(requests.get(url, stream=True).raw)
    return data

st.header("My Most Recent Orders")

#get the user id
userID = select(User.id) #.where(User.id = this.id) parang ganun di ko ma figure out to

#get the orders the user has made
queryOrders = select(Order.id, Order.address, Order.barangay, Order.city).where(Order.ordered_by == userID, Order.ordered_by == User.id) #again, not sure kung gagana to
ordersList = db.execute(queryOrders)

#get the details of each order
#ideally we order this by most recent but we don't have date saved for the orders
queryFlowerOrders = select(Order.id, OrderFlower.flower_name, OrderFlower.quantity).where(Order.ordered_by == User.id, Order.id == OrderFlower.order_id, User.id == userID)
queryBouquetOrders = select(Order.id, OrderBouquet.bouquet_name, OrderBouquet.quantity).where(Order.ordered_by == User.id, Order.id == OrderBouquet.order_id, User.id == userID)
orderDetails = db.execute(queryFlowerOrders).all() + db.execute(queryBouquetOrders).all() #idk if this works like this

myOrders = st.container(key="my orders")

with myOrders:
    cols = st.columns(
        len(ordersList), gap="small", border=True
    )
    i = 0
    for id in ordersList:
        with cols[i]:
            st.subheader(f"Order IDL {id}")
            for flower_name, quantity in orderDetails:
                st.write(f"{flower_name} — {quantity}")
            for bouquet_name, quantity in orderDetails:
                st.write(f"{bouquet_name} — {quantity}")
        i += 1

custom_css = """
<style>
    .st-key-my-orders [data-testid="stColumn"]{
        background-color: white;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)