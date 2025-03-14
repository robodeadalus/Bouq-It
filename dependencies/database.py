from typing import Iterable, Optional

from sqlalchemy import CheckConstraint, Float, ForeignKey, Integer, Sequence, String
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


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
    )
    email: Mapped[str] = mapped_column(String(255))
    password: Mapped[str] = mapped_column(String(255))
    last_name: Mapped[str] = mapped_column(String(255))
    first_name: Mapped[str] = mapped_column(String(255))
    middle_name: Mapped[Optional[str]]
    contact: Mapped[str] = mapped_column(String(255))
    address: Mapped[str] = mapped_column(String(255))
    barangay: Mapped[str] = mapped_column(String(255))
    city: Mapped[str] = mapped_column(String(255))
    zipcode: Mapped[str] = mapped_column(String(255))

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
            "IN ('G-Cash', 'Maya', 'Cash on Delivery', 'Credit/Debit Card')",
            name="orders_payment_check",
        ),
    )
    address: Mapped[str] = mapped_column(String(255))
    barangay: Mapped[str] = mapped_column(String(255))
    city: Mapped[str] = mapped_column(String(255))
    zipcode: Mapped[str] = mapped_column(String(255))
    ordered_by: Mapped[int] = mapped_column(Integer(), ForeignKey("customers.id"))

    def __repr__(self) -> str:
        return f"Order(id={self.id!r}, ordered_by={self.ordered_by!r})"


class Flower(Base):
    __tablename__ = "flowers"

    name: Mapped[str] = mapped_column(
        String(255),
        primary_key=True,
        unique=True,
    )
    description: Mapped[str] = mapped_column(TEXT())
    short_desc: Mapped[str] = mapped_column(TEXT())
    image_link: Mapped[str] = mapped_column(TEXT())
    origin: Mapped[str] = mapped_column(TEXT())
    meaning: Mapped[str] = mapped_column(TEXT())
    price: Mapped[float] = mapped_column(Float(2))

    def __repr__(self) -> str:
        return f"Flower(name={self.name!r}, price={self.price!r})"


class Bouquet(Base):
    __tablename__ = "bouquets"

    bouquet_name: Mapped[str] = mapped_column(
        String(255),
        primary_key=True,
        unique=True,
    )
    description: Mapped[str] = mapped_column(TEXT())
    short_desc: Mapped[str] = mapped_column(TEXT())
    image_link: Mapped[str] = mapped_column(TEXT())
    origin: Mapped[str] = mapped_column(TEXT())
    meaning: Mapped[str] = mapped_column(TEXT())
    price: Mapped[float] = mapped_column(Float(2))

    def __repr__(self) -> str:
        return f"Bouquet(name={self.bouquet_name!r}, price={self.price!r})"


class BouquetFlower(Base):
    __tablename__ = "bouquet_flowers"

    bouquet_name: Mapped[str] = mapped_column(
        String(255),
        ForeignKey("bouquets.id"),
        primary_key=True,
    )
    flower_name: Mapped[str] = mapped_column(
        String(255),
        ForeignKey("flowers.name"),
        primary_key=True,
    )
    quantity: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint("quantity >= 1"),
    )

    def __repr__(self) -> str:
        return f"Bouquet Flower(Bouquet={self.bouquet_name!r}, Flower={self.flower_name!r})"


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
        Integer,
        CheckConstraint("quantity >= 1"),
    )

    def __repr__(self) -> str:
        return (
            f"Flower Order(Ordered by={self.order_id!r}, Ordered={self.flower_name!r})"
        )


class OrderBouquet(Base):
    __tablename__ = "order_bouquets"

    order_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("orders.id"),
        primary_key=True,
    )
    bouquet_name: Mapped[str] = mapped_column(
        String(255),
        ForeignKey("bouquets.bouquet_name"),
        primary_key=True,
    )
    quantity: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint("quantity >= 1"),
    )
    design: Mapped[Optional[str]]

    def __repr__(self) -> str:
        return f"Buoquet Order(Ordered by={self.order_id!r}, Ordered={self.bouquet_name!r})"


class Shop(Base):
    __tablename__ = "shops"
    id: Mapped[int] = mapped_column(
        Sequence("shops_id_seq"),
        primary_key=True,
        unique=True,
    )
    name: Mapped[str] = mapped_column(String(255))
    address: Mapped[str] = mapped_column(String(255))
    barangay: Mapped[str] = mapped_column(String(255))
    city: Mapped[str] = mapped_column(String(255))
    zipcode: Mapped[str] = mapped_column(String(255))
    contact: Mapped[str] = mapped_column(String(255))
    sales: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint("quantity >= 0"),
    )

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
        Integer,
        CheckConstraint("quantity >= 0"),
    )

    def __repr__(self) -> str:
        return f"Flower Shop(Shop ID={self.shop_id!r}, Flower={self.flower_name!r})"


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
        Integer,
        CheckConstraint("quantity >= 0"),
    )

    def __repr__(self) -> str:
        return f"Bouquet Shop(Shop ID={self.shop_id!r}, Bouquet={self.bouquet_name!r})"
