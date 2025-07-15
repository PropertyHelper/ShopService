import uuid

from pydantic import BaseModel

from src.core.models import Item


class ShopItems(BaseModel):
    items: list[Item]
    total: int

class ShopNames(BaseModel):
    names: list[str]

class SelectedItems(BaseModel):
    item_id_list: list[uuid.UUID]
