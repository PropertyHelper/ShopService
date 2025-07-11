import uuid

from pydantic import BaseModel, Field


class ShopCreate(BaseModel):
    nickname: str
    password: str

class ShopSave(ShopCreate):
    sid: uuid.UUID

class Shop(BaseModel):
    sid: uuid.UUID
    nickname: str

class CashierCreate(BaseModel):
    account_name: str
    shop_id: uuid.UUID
    password: str

class CashierSave(CashierCreate):
    cid: uuid.UUID

class Cashier(BaseModel):
    cid: uuid.UUID
    account_name: str
    shop_id: uuid.UUID

class ItemCreate(BaseModel):
    name: str
    description: str
    photo_url: str | None = None
    price: int = Field(gt=0)
    percent_point_allocation: int = Field(ge=0)
    shop_id: uuid.UUID

class Item(ItemCreate):
    iid: uuid.UUID

class ShopLogInRequest(BaseModel):
    nickname: str
    password: str

class CashierLoginRequest(BaseModel):
    shop_nickname: str
    account_name: str
    password: str
