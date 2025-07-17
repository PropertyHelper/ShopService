import uuid

from fastapi import APIRouter, Depends, HTTPException

from src.api.v1.dependencies import get_item_service
from src.api.v1.models import SelectedItems
from src.core.models import Item, ItemCreate
from src.core.services.item import ItemService

router = APIRouter()

@router.get("/item/{uid}")
async def get_item(uid: uuid.UUID, item_service: ItemService = Depends(lambda: get_item_service())) -> Item:
    """
    Get an item bu its id

    :param uid: item id
    :param item_service: Injected item service
    :return: Item domain model
    :raise HTTPException if item was not found
    """
    item = await item_service.get_item(uid)
    if item is None:
        raise HTTPException(status_code=404)
    return item

@router.post("/item")
async def add_item(item_create: ItemCreate, item_service: ItemService = Depends(lambda: get_item_service())) -> Item:
    """
    Save single item for a shop.

    :param item_create: a model for creating items
    :param item_service: Injected item service
    :return: item domain model
    """
    item = await item_service.add_item(item_create)
    return item

@router.post("/items")
async def add_items(item_create_list: list[ItemCreate], item_service: ItemService = Depends(lambda: get_item_service())) -> list[Item]:
    """
   Save multiple items for a shop.

   :param item_create_list: a list of models for creating items
   :param item_service: Injected item service
   :return: list of item domain models
   """
    items = await item_service.add_items(item_create_list)
    return items

@router.post("/items/get")
async def get_items(item_id_list:  SelectedItems, item_service: ItemService = Depends(lambda: get_item_service())) -> list[Item]:
    """
    Get items by their ids.

    :param item_id_list: list of item id
    :param item_service: Injected item service
    :return: list of item domain models
    """
    item = await item_service.get_items(item_id_list.item_id_list)
    if item is None:
        raise HTTPException(status_code=404)
    return item