import streamlit as st

st.title("Flower Catalogue")

st.header("Flowers")

st.markdown(
    """
    <style>
        /* Adjust the font size of subheaders within columns */
        .custom-subheader {
            font-size: 20px;
            font-weight: bold;
        }
        .hover-column {
            padding: 10px;
            border-radius: 5px;
            transition: background-color 0.3s;
        }
        .hover-column:hover {
            background-color: rgba(0, 0, 0, 0.05);
        }
    </style>
    """,
    unsafe_allow_html=True,
)

flowers = st.container()
with flowers:
    col = st.columns(4, gap="small", border=True)
    with col[0]:
        st.image(
            "https://catherinephillips.com.au/cdn/shop/files/E3C177A5-0F3C-4AB4-B206-8A0043849DF8.jpg?v=1717699718&width=1946"
        )
        st.markdown(
            '<p class="custom-subheader">Chrysanthemum</p>', unsafe_allow_html=True
        )
    with col[1]:
        st.image(
            "https://prestigebotanicals.com/cdn/shop/files/PF15-Blush-Real-Touch-Rose.jpg?v=1708631940&width=800"
        )
        st.markdown('<p class="custom-subheader">Pink Rose</p>', unsafe_allow_html=True)
    with col[2]:
        st.image(
            "https://flowerranchcafe.com/cdn/shop/products/DSCF9138.jpg?v=1681202897&width=1946",
            width=150,
        )
        st.markdown(
            '<p class="custom-subheader">Carnations</p>', unsafe_allow_html=True
        )
    with col[3]:
        st.image(
            "https://www.carolinefineflowers.co.za/cdn/shop/files/7_a3ed9173-5c49-4473-8abd-e27acc525abc.jpg?v=1737975360"
        )
        st.markdown(
            '<p class="custom-subheader">Sunflowers</p>', unsafe_allow_html=True
        )
