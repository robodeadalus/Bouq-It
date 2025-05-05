from PIL import Image
from sqlalchemy import select

from dependencies.database import *
from dependencies.helper import fetch

db: Session = st.session_state["db"]
st.title("Homepage")

search_bar = st.text_input("none", placeholder="Search", label_visibility="hidden")

selection = st.selectbox(
    "Filter by:",
    (
        "Shops",
        "Flowers",
        "Location",
        "Price: Ascending",
        "Price Descending",
        "Color",
        "Occasion",
    ),
)

st.header("Best-Selling Flower Shops")

queryShop = select(Shop).order_by(Shop.sales.desc()).limit(3)
topShops: Sequence[Shop] = db.execute(queryShop).scalars().all()

bestShop = st.container(
    key="best shop",
)

topShopDict = {shop.name: shop for shop in topShops}
with bestShop:
    cols = st.columns(
        len(topShops), gap="small", border=True
    )  # Adjust for available shops
    i = 0
    for shop in topShops:
        with cols[i]:
            shopImage = topShopDict.get(shop.name)
            st.image(
                shopImage.image_link, use_container_width=True
            )  # Replace with actual shop images
            st.subheader(shop.name, anchor=False)
            # st.write(f"Sales: {shop.sales}")
            if st.button(
                f"View",
                key=f"shop_{shop.id}",
                use_container_width=True,
                type="primary",
            ):
                st.session_state["selected_shop_id"] = shop.id
                st.switch_page("pages/_shop_detail.py")
        i += 1


# Best-Selling Flowers
st.header("Best-Selling Flowers")
queryFlowers = (
    select(Flower)
    .join(OrderFlower, Flower.name == OrderFlower.flower_name)
    .order_by(OrderFlower.quantity.desc())
    .limit(4)
)
topFlowers = db.execute(queryFlowers).scalars().all()


@st.dialog("Flower Details")
def show_flower_details(flower):
    st.write(f"**Price:** ₱{flower.price:.2f}")
    st.write(f"**Origin:** {flower.origin}")
    st.write(f"**Meaning:** {flower.meaning}")
    st.write(f"**Description:** {flower.description}")


bestFlower = st.container(key="best flower")
with bestFlower:
    cols = st.columns(
        len(topFlowers), gap="small", border=True
    )  # Adjust for available data
    i = 0
    for flower in topFlowers:
        with cols[i]:
            st.image(flower.image_link, use_container_width=True)
            st.subheader(flower.name)
            if st.button(
                f"View",
                key=f"view_button_{i}",
                use_container_width=True,
                type="primary",
            ):
                show_flower_details(flower)
        i += 1

custom_css = """
<style>
    .st-key-best-shop [data-testid="stColumn"]{
        background-color: white;
    }
    .st-key-best-flower [data-testid="stColumn"] {
        background-color: white;
    }
    div[class*="st-key-shop_"] {
    }
    h3 {
        height: 5.5rem;
        overflow: hidden;
        white-space: pre-wrap;
        text-overflow: ellipsis;
        word-break: initial;
    }
    
    img {
    height: 200px;
    width: 100%;
    object-fit: cover;
    border-radius: 10px;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)
