import uuid

from pydantic import BaseModel, Field


class ShopCreate(BaseModel):
    """
    Use to create the shop
    """
    nickname: str
    password: str

class ShopSave(ShopCreate):
    """
    Use to save the shop (by infrastructure level)
    """
    sid: uuid.UUID

class Shop(BaseModel):
    """
    Use to represent shop in the domain
    """
    sid: uuid.UUID
    nickname: str

class CashierCreate(BaseModel):
    """
    Use to create the cashier
    """
    account_name: str
    shop_id: uuid.UUID
    password: str

class CashierSave(CashierCreate):
    """
    Use to save the cashier (by infrastructure level)
    """
    cid: uuid.UUID

class Cashier(BaseModel):
    """Use to represent the cashier domain model"""
    cid: uuid.UUID
    account_name: str
    shop_id: uuid.UUID

class ItemCreate(BaseModel):
    """
    Use to create an item

    Rules enforced:
        - price must be positive
        - percent point allocation is not negative
    Note:
        - It is expected to provide data in fills (0.01 AED)
          to avoid rounding errors
    """
    name: str
    description: str
    photo_url: str | None = None
    price: int = Field(gt=0)
    percent_point_allocation: int = Field(ge=0)
    shop_id: uuid.UUID

class Item(ItemCreate):
    """Use to represent the item domain model (or save)"""
    iid: uuid.UUID

class ShopLogInRequest(BaseModel):
    """Use to provide credentials to shop login endpoint"""
    nickname: str
    password: str

class CashierLoginRequest(BaseModel):
    """Use to provide credentials to cashier login endpoint"""
    shop_nickname: str
    account_name: str
    password: str
