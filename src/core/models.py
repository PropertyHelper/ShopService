import uuid

from pydantic import BaseModel, Field

class Shop(BaseModel):
    sid: uuid.UUID
    nichname: str

class ShopCreate(Shop):
    password: str

class Cashier(BaseModel):
    cid: uuid.UUID
    account_name: str
    shop_id: uuid.UUID

class CashierCreate(Cashier):
    password: str

class Item(BaseModel):
    iid: uuid.UUID
    name: str
    description: str
    photo_url: str | None = None
    price: int = Field(gt=0)
    percent_point_allocation: int = Field(ge=0)
    shop_id: uuid.UUID


class ShopLogInRequest(BaseModel):
    nickname: str
    password: str

class CashierLoginRequest(BaseModel):
    shop_nickname: str
    account_name: str
    password: str
