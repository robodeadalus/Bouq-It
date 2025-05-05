# pages/myorders.py

import pandas as pd
import streamlit as st
from sqlalchemy import desc, func, select
from sqlalchemy.orm import aliased

from dependencies.database import *

# Authentication check

if not st.session_state.get("authentication_status", False):

    st.switch_page("pages/homepage.py")


if "user_id" not in st.session_state:

    st.warning("Please login to view orders")

    st.stop()


db: Session = st.session_state["db"]


st.title("My Orders")


def get_user_orders(user_id: int):

    OrderAlias = aliased(Order)

    CQ = aliased(CustomBouquet)

    # build total = sum(flowers) + sum(bouquets) + sum(custom prices)

    total_expr = (
        func.coalesce(func.sum(OrderFlower.quantity * Flower.price), 0)
        + func.coalesce(func.sum(OrderBouquet.quantity * Bouquet.price), 0)
        + func.coalesce(func.sum(CQ.price), 0)
    ).label("total")

    stmt = (
        select(
            OrderAlias.id.label("id"),
            OrderAlias.payment.label("payment"),
            OrderAlias.order_date.label("order_date"),
            total_expr,
        )
        .select_from(OrderAlias)
        .outerjoin(OrderFlower, OrderAlias.id == OrderFlower.order_id)
        .outerjoin(Flower, OrderFlower.flower_name == Flower.name)
        .outerjoin(OrderBouquet, OrderAlias.id == OrderBouquet.order_id)
        .outerjoin(Bouquet, OrderBouquet.bouquet_name == Bouquet.name)
        .outerjoin(OrderCustom, OrderAlias.id == OrderCustom.order_id)
        .outerjoin(CQ, OrderCustom.custom_bouquet == CQ.bouquet_name)
        .where(OrderAlias.ordered_by == user_id)
        .group_by(OrderAlias.id, OrderAlias.payment, OrderAlias.order_date)
        .order_by(desc(OrderAlias.order_date))
    )

    orders = db.execute(stmt).all()

    # fetch the line-items per order

    order_details = {}

    for row in orders:

        oid = row.id

        items = []

        # flowers

        for of, fl in db.execute(
            select(OrderFlower, Flower)
            .join(Flower, OrderFlower.flower_name == Flower.name)
            .where(OrderFlower.order_id == oid)
        ):

            items.append(
                {
                    "Type": "Flower",
                    "Name": fl.name,
                    "Quantity": of.quantity,
                    "Unit Price": float(fl.price),
                    "Total": float(fl.price) * of.quantity,
                }
            )

        # bouquets

        for ob, bq in db.execute(
            select(OrderBouquet, Bouquet)
            .join(Bouquet, OrderBouquet.bouquet_name == Bouquet.name)
            .where(OrderBouquet.order_id == oid)
        ):

            line = float(bq.price) * ob.quantity

            items.append(
                {
                    "Type": "Bouquet",
                    "Name": bq.name + (f" ({ob.design})" if ob.design else ""),
                    "Quantity": ob.quantity,
                    "Unit Price": float(bq.price),
                    "Total": line,
                }
            )

        # custom
        for oc, cq in db.execute(
            select(OrderCustom, CQ)
            .join(CQ, OrderCustom.custom_bouquet == CQ.bouquet_name)
            .where(OrderCustom.order_id == oid)
        ):

            items.append(
                {
                    "Type": "Custom Bouquet",
                    "Name": cq.bouquet_name + (f" ({cq.design})" if cq.design else ""),
                    "Quantity": 1,
                    "Unit Price": float(cq.price),
                    "Total": float(cq.price),
                }
            )

        order_details[oid] = items

    return orders, order_details


orders, order_details = get_user_orders(st.session_state.user_id)

if not orders:
    st.info("You haven't placed any orders yet")
    st.stop()


for order in orders:

    with st.expander(f"## **Order #{order.id} — {order.order_date:%Y-%m-%d %H:%M}**"):
        st.write(f"**Order Date:** {order.order_date:%b %d, %Y %I:%M %p}")
        st.write(f"**Payment Method:** {order.payment}")
        st.write(f"**Total:** ₱{order.total:.2f}")
        st.subheader("Order Items", anchor=False)

        # build a DataFrame for this order's items
        df_items = pd.DataFrame(order_details[order.id]).reset_index(drop=True)
        # format currency columns
        df_items["Unit Price"] = df_items["Unit Price"].map(lambda v: f"₱{v:.2f}")
        df_items["Total"] = df_items["Total"].map(lambda v: f"₱{v:.2f}")

        # show without the index
        st.dataframe(df_items, use_container_width=True)
