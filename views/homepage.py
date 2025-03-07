import streamlit as st

st.title("Homepage")

search_bar = st.text_input("none", placeholder="Search", label_visibility="hidden")


st.header("Best-Selling Flower Shops")
shopNames = ["Corpuz Crops", "Onym's Flowerfest", "Boutiqa ni Gab", "Miks-n-Match Flowery"]
shopSales = [5000, 7000, 6000, 8000]

bestShop = st.container(key="best shop")
with bestShop:
    cols = st.columns(4, gap="small", border=True)  # Adjust the number for layout
    for i, shop in enumerate(shopNames):  
        with cols[i]:
            st.image("https://picsum.photos/400/500")
            st.subheader(shop)
            st.write(f"Sales: {shopSales[i]}")


# Best-Selling Flowers
st.header("Best-Selling Flowers")
flowerNames = ["Pastel Delight", "Pinky-pie", "Super-duper Red Flower", "Cool Flower Name"]
flowerSales = [9000, 8500, 7800, 8200] 

bestFlower = st.container(key="best flower")
with bestFlower:
    cols = st.columns(4, gap="small", border=True)
    for i, flower in enumerate(flowerNames):  # Placeholder for 4 flowers
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
