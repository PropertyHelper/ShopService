import uuid

from pydantic import BaseModel

from src.core.models import Item


class ShopItems(BaseModel):
    """
    Use to return a list of items.

    Created to ensure later extendability without breaking changes.
    """
    items: list[Item]
    total: int

class ShopNames(BaseModel):
    """
    Use to return a list of shop names.

    Created to ensure later extendability without breaking changes.
    """
    names: list[str]

class SelectedItems(BaseModel):
    """
    Use to get a list of item ids.

    Created to ensure later extendability without breaking changes.
    """
    item_id_list: list[uuid.UUID]
