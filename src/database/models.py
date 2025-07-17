import datetime
import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy models.

    Provides common functionality and metadata for all database entities.
    """
    pass

class Shop(Base):
    """
    Encapsulate shop data.

    Use nickname to refer to the shop instead of sid.
    """
    __tablename__ = "shops"
    sid: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    nickname: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str]
    joined_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now)

class Cashier(Base):
    """
    Encapsulate the cashier data.

    account_name is not expected to be unique throughought the database,
    but the business logic layer is assummed to ensure that within one shop
    all cashiers have different accounts
    """
    __tablename__ = "cashiers"
    cid: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    account_name: Mapped[str]
    password_hash: Mapped[str]
    created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now)
    shop_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("shops.sid"))

class Item(Base):
    """
    Encapsulate items.

    Store data essnetial to display the item by the cashier software later.
    Note:
        - price is expected to be in fills (0.01 AED) to avoid rounding errors.
    """
    __tablename__ = "items"
    iid: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str] = mapped_column(nullable=True)
    photo_url: Mapped[str] = mapped_column(nullable=True)
    price: Mapped[int]
    percent_point_allocation: Mapped[int]
    shop_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("shops.sid"))
