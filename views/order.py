import streamlit as st

st.title("Order Page")

search_bar = st.text_input("none", placeholder="Search", label_visibility="hidden")

#Available Flowers
st.header("Available Flowers and Bouquets")
flowerNames = ["Pastel Delight", "Pinky-pie", "Super-duper Red Flower", "Cool Flower Name"]
flowerPrices = [50, 40, 55, 100] 

availableFlower = st.container(key="available flower")
with availableFlower:
    cols = st.columns(4, gap="small", border=True)
    for i, flower in enumerate(flowerNames):  # Placeholder for 4 flowers
        with cols[i]:
            st.image("https://picsum.photos/400/500")
            st.subheader(flower)
            st.write(f"Price: P{flowerPrices[i]}")
            st.button("", icon=":material/add_circle:", key=f"add_{i}")

custom_css = """
<style>
    .st-key-available-shop .stColumn{
        background-color: white;
    }
    .st-key-available-flower [data-testid="stColumn"] {
        background-color: white;
    }
    .st-key-available-flower button {
        background-color: white !important;
        margin-top: -50px !important; 
        float: right;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)