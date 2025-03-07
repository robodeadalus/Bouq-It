import streamlit as st

st.title("Flower Catalogue")

st.header("Flowers")

# st.markdown(
#     """
#     <style>
#         /* Adjust the font size of subheaders within columns */
#         .custom-subheader {
#             font-size: 20px;
#             font-weight: bold;
#         }
#         .dropdown {
#             position: relative;
#             display: inline-block;
#         }

#         .dropdown-content [data-testid="stHorizontalBlock"] {
#             display: none;
#             position: absolute;
#             background-color: #f9f9f9;
#             min-width: 160px;
#             box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
#             z-index: 1;
#         }

#         .dropdown:hover .dropdown-content {
#             display: block;
#         }

#         .desc {
#             padding: 15px;
#             text-align: center;
#         }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

flowers = st.container(key = "flowers")
with flowers:
    col = st.columns(4, gap="small", border=True)
    with col[0]:
        st.image(
            "https://catherinephillips.com.au/cdn/shop/files/E3C177A5-0F3C-4AB4-B206-8A0043849DF8.jpg?v=1717699718&width=1946"
        )
        st.subheader("Chrysanthemum")
        st.markdown('<p class="dropdown-content"> Native to East Asia</p>', unsafe_allow_html=True)
    with col[1]:
        st.image(
            "https://prestigebotanicals.com/cdn/shop/files/PF15-Blush-Real-Touch-Rose.jpg?v=1708631940&width=800"
        )
        st.subheader("Pink Rose")
    with col[2]:
        st.image(
            "https://flowerranchcafe.com/cdn/shop/products/DSCF9138.jpg?v=1681202897&width=1946",
            width=150,
        )
        st.subheader("Carnations")
    with col[3]:
        st.image(
            "https://www.carolinefineflowers.co.za/cdn/shop/files/7_a3ed9173-5c49-4473-8abd-e27acc525abc.jpg?v=1737975360"
        )
        st.subheader("Sunflower")


custom_css = """
<style>
    div[data-testid="stColumn"] {
        display: flex;
        color: green
    }
    .dropdown {
        position: relative;
        display: inline-block;
    }
    .dropdown-content {
        display: none;
        position: absolute;
        background-color: white;
        max-width: 200px;
        z-index: 1;
    }
    .dropdown:hover .dropdown-content {
        display: block;
    }
    .desc {
        padding: 10px;
        text-align: center;
    }
    .st-key-flowers .stColumn  {
        background-color: white;
    }
    .st-key-flowers [data-testid="stHorizontalBlock"] {
        padding: 10px;
        border-radius: 5px;
        transition: background-color 0.3s;
    }
    
    .hover-column:hover {
        background-color: rgba(0, 0, 0, 0.05);
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)