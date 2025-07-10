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
    __tablename__ = "shops"
    sid: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    password_hash: Mapped[str]
    joined_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now)

class Cashier(Base):
    __tablename__ = "cashiers"
    cid: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    password_hash: Mapped[str]
    created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now)
    shop_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("shops.sid"))

class Item(Base):
    __tablename__ = "items"
    iid: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    photo_url: Mapped[str]
    price: Mapped[int]
    percent_point_allocation: Mapped[int]
    shop_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("shops.sid"))
