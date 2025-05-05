from typing import Iterable, Optional

import streamlit as st
from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    Numeric,
    Sequence,
    String,
    func,
)
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


@st.cache_resource
def db_connect():
    # Ensure the session uses Asia/Manila timezone (GMT+8)
    db = st.connection(
        "postgresql",
        type="sql",
    )
    return db.engine, db.session


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(
        Sequence("customers_id_seq"),
        primary_key=True,
        unique=True,
    )
    username: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    middle_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    contact: Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    barangay: Mapped[str] = mapped_column(String(255), nullable=False)
    city: Mapped[str] = mapped_column(String(255), nullable=False)
    zipcode: Mapped[str] = mapped_column(String(255), nullable=False)

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.first_name!r} {self.last_name!r})"


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(
        Sequence("orders_id_seq"), primary_key=True, unique=True
    )
    payment: Mapped[str] = mapped_column(
        String(255),
        CheckConstraint(
            "payment IN ('G-Cash', 'Maya', 'Cash on Delivery', 'Credit/Debit Card')",
            name="orders_payment_check",
        ),
        nullable=False,
    )
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    barangay: Mapped[str] = mapped_column(String(255), nullable=False)
    city: Mapped[str] = mapped_column(String(255), nullable=False)
    zipcode: Mapped[str] = mapped_column(String(255), nullable=False)
    ordered_by: Mapped[int] = mapped_column(
        Integer(), ForeignKey("customers.id"), nullable=False
    )
    order_date: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    def __repr__(self) -> str:
        return f"Order(id={self.id!r}, ordered_by={self.ordered_by!r}, date={self.order_date!r})"


class Flower(Base):
    __tablename__ = "flowers"

    name: Mapped[str] = mapped_column(
        String(255),
        primary_key=True,
        unique=True,
    )
    description: Mapped[str] = mapped_column(TEXT(), nullable=False)
    short_desc: Mapped[str] = mapped_column(TEXT(), nullable=False)
    image_link: Mapped[str] = mapped_column(TEXT(), nullable=False)
    origin: Mapped[str] = mapped_column(TEXT(), nullable=False)
    meaning: Mapped[str] = mapped_column(TEXT(), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    def __repr__(self) -> str:
        return f"Flower(name={self.name!r}, price={self.price!r})"


class Bouquet(Base):
    __tablename__ = "bouquets"

    name: Mapped[str] = mapped_column(
        String(255),
        primary_key=True,
        unique=True,
    )
    description: Mapped[str] = mapped_column(TEXT(), nullable=False)
    short_desc: Mapped[str] = mapped_column(TEXT(), nullable=False)
    image_link: Mapped[str] = mapped_column(TEXT(), nullable=False)
    origin: Mapped[str] = mapped_column(TEXT(), nullable=False)
    meaning: Mapped[str] = mapped_column(TEXT(), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    def __repr__(self) -> str:
        return f"Bouquet(name={self.name!r}, price={self.price!r})"


class BouquetFlower(Base):
    __tablename__ = "bouquet_flowers"

    bouquet_name: Mapped[str] = mapped_column(
        String(255),
        ForeignKey("bouquets.name"),
        primary_key=True,
    )
    flower_name: Mapped[str] = mapped_column(
        String(255),
        ForeignKey("flowers.name"),
        primary_key=True,
    )
    quantity: Mapped[int] = mapped_column(
        Integer, CheckConstraint("quantity >= 1"), nullable=False
    )

    def __repr__(self) -> str:
        return (
            f"BouquetFlower(Bouquet={self.bouquet_name!r}, Flower={self.flower_name!r})"
        )


class OrderFlower(Base):
    __tablename__ = "order_flowers"

    order_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("orders.id"),
        primary_key=True,
    )
    flower_name: Mapped[str] = mapped_column(
        String(255),
        ForeignKey("flowers.name"),
        primary_key=True,
    )
    quantity: Mapped[int] = mapped_column(
        Integer, CheckConstraint("quantity >= 1"), nullable=False
    )

    def __repr__(self) -> str:
        return f"OrderFlower(order_id={self.order_id!r}, flower={self.flower_name!r})"


class OrderBouquet(Base):
    __tablename__ = "order_bouquets"

    order_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("orders.id"),
        primary_key=True,
    )
    bouquet_name: Mapped[str] = mapped_column(
        String(255),
        ForeignKey("bouquets.name"),
        primary_key=True,
    )
    quantity: Mapped[int] = mapped_column(
        Integer, CheckConstraint("quantity >= 1"), nullable=False
    )
    design: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    def __repr__(self) -> str:
        return (
            f"OrderBouquet(order_id={self.order_id!r}, bouquet={self.bouquet_name!r})"
        )


class Shop(Base):
    __tablename__ = "shops"
    id: Mapped[int] = mapped_column(
        Sequence("shops_id_seq"),
        primary_key=True,
        unique=True,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    barangay: Mapped[str] = mapped_column(String(255), nullable=False)
    city: Mapped[str] = mapped_column(String(255), nullable=False)
    zipcode: Mapped[str] = mapped_column(String(255), nullable=False)
    contact: Mapped[str] = mapped_column(String(255), nullable=False)
    sales: Mapped[int] = mapped_column(
        Integer, CheckConstraint("sales >= 0"), nullable=False
    )
    image_link: Mapped[str] = mapped_column(TEXT(), nullable=False)

    def __repr__(self) -> str:
        return f"Shop(id={self.id!r})"


class ShopFlower(Base):
    __tablename__ = "shop_flowers"

    shop_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("shops.id"),
        primary_key=True,
    )
    flower_name: Mapped[str] = mapped_column(
        String(255),
        ForeignKey("flowers.name"),
        primary_key=True,
    )
    quantity: Mapped[int] = mapped_column(
        Integer, CheckConstraint("quantity >= 0"), nullable=False
    )

    def __repr__(self) -> str:
        return f"ShopFlower(shop_id={self.shop_id!r}, flower={self.flower_name!r})"


class ShopBouquet(Base):
    __tablename__ = "shop_bouquets"

    shop_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("shops.id"),
        primary_key=True,
    )
    bouquet_name: Mapped[str] = mapped_column(
        String(255),
        ForeignKey("bouquets.name"),
        primary_key=True,
    )
    quantity: Mapped[int] = mapped_column(
        Integer, CheckConstraint("quantity >= 0"), nullable=False
    )

    def __repr__(self) -> str:
        return f"ShopBouquet(shop_id={self.shop_id!r}, bouquet={self.bouquet_name!r})"


class CustomerFlower(Base):
    __tablename__ = "customer_flowers"

    customer_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("customers.id"),
        primary_key=True,
    )
    flower_name: Mapped[str] = mapped_column(
        String(255),
        ForeignKey("flowers.name"),
        primary_key=True,
    )
    quantity: Mapped[int] = mapped_column(
        Integer, CheckConstraint("quantity >= 1"), nullable=False
    )

    def __repr__(self) -> str:
        return f"CustomerFlower(customer_id={self.customer_id!r}, flower={self.flower_name!r}, qty={self.quantity!r})"


class CustomerBouquet(Base):
    __tablename__ = "customer_bouquets"

    customer_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("customers.id"),
        primary_key=True,
    )
    bouquet_name: Mapped[str] = mapped_column(
        String(255),
        ForeignKey("bouquets.name"),
        primary_key=True,
    )
    quantity: Mapped[int] = mapped_column(
        Integer, CheckConstraint("quantity >= 1"), nullable=False
    )
    design: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    def __repr__(self) -> str:
        return f"CustomerBouquet(customer_id={self.customer_id!r}, bouquet={self.bouquet_name!r}, qty={self.quantity!r})"


class CustomBouquet(Base):
    __tablename__ = "custom_bouquets"

    customer_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("customers.id"),
        primary_key=True,
    )

    bouquet_name: Mapped[str] = mapped_column(
        String(255),
        primary_key=True,
    )

    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    design: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    def __repr__(self) -> str:
        return f"CustomBouquet(customer_id={self.customer_id!r}, bouquet={self.bouquet_name!r}, price={self.price!r})"


class OrderCustom(Base):
    __tablename__ = "order_custom"

    order_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("orders.id"),
        primary_key=True,
    )

    custom_bouquet: Mapped[str] = mapped_column(
        String(255),
        primary_key=True,
    )

    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    def __repr__(self) -> str:
        return f"OrderCustom(order_id={self.order_id!r}, custom_bouquet={self.custom_bouquet!r})"
