import streamlit as st

st.title("Homepage")

search_bar = st.text_input("none", placeholder="Search", label_visibility="hidden")

st.header("Best-Selling Flower Shops")

bestShop = st.container(key="best shop")
with bestShop:
    cols = st.columns(4, gap="small", border=True)  # Adjust the number for layout
    for i in range(4):  # Placeholder for 4 shops
        with cols[i]:
            st.image("https://picsum.photos/400/500")
            st.subheader(f"Shop {i+1}")
            st.write(f"{i * 1000 + 3000}")


# Best-Selling Flowers
st.header("Best-Selling Flowers")

bestFlower = st.container(key="best flower")
with bestFlower:
    cols = st.columns(4, gap="small", border=True)
    for i in range(4):  # Placeholder for 4 flowers
        with cols[i]:
            st.image("https://picsum.photos/400/500")
            st.subheader(f"Shop {i+1}")
            st.write(f"{i * 1000 + 3000}")

custom_css = """
<style>
    .st-key-best-shop [data-testid="stColumn"] {
        background-color: white;
    }
    .st-key-best-flower [data-testid="stColumn"] {
        background-color: white;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)
