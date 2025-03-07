import streamlit as st

st.title("Order Page")

# Create three columns with the first one taking most of the space
empty_space, button1, button2 = st.columns([4, 1, 1])

# Add buttons to the second and third columns
with button1:
    st.button("View Cart", key="view cart")
with button2:
    st.button("Checkout", key="checkout")

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
    .st-key-view-cart button, .st-key-checkout button {
        font-weight: bold !important;
        background-color: white !important;
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