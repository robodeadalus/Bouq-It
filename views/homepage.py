import streamlit as st

st.markdown("<h1 style='color: #514743;'>HOMEPAGE</h1>", unsafe_allow_html=True)

search_bar = st.text_input("none", placeholder="Search", label_visibility="hidden")

st.markdown(
    """
    <style>
        .block-container {
            
        }
        .card {
            background-color: white;
            border-radius: 15px;
            padding: 15px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            text-align: center;
            margin: 10px;
        }
        .card img {
            border-radius: 10px;
            width: 100%;
            height: auto;
        }
        .card-container {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-around;
        }
    </style>
""",
    unsafe_allow_html=True,
)
st.markdown(
    "<h3 style='color: #514743;'>Best-Selling Flower Shops</h3>", unsafe_allow_html=True
)
cols = st.columns(4)  # Adjust the number for layout


for i in range(4):  # Placeholder for 4 shops
    with cols[i]:
        st.markdown(
            f"""
            <div class="card">
                <img src="https://picsum.photos/400/500" alt="Shop Image">
                <h4 style="color: #514743;">Shop {i+1}</h4>
                <p style="color: #514743;">{i * 1000 + 3000} Sales</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

# Best-Selling Flowers
st.markdown(
    "<h3 style='color: #514743;'>Best-Selling Flowers</h3>", unsafe_allow_html=True
)
cols = st.columns(4)

for i in range(4):  # Placeholder for 4 flowers
    with cols[i]:
        st.markdown(
            f"""
            <div class="card">
                <img src="https://picsum.photos/400/500" alt="Flower Image">
                <h4 style="color: #514743;">Shop {i+1}</h4>
                <p style="color: #514743;">{i * 1000 + 3000} Sales</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
