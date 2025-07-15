import uuid

from fastapi import APIRouter, Depends, HTTPException

from src.api.v1.dependencies import get_item_service
from src.api.v1.models import SelectedItems
from src.core.models import Item, ItemCreate
from src.core.services.item import ItemService

router = APIRouter()

@router.get("/item/{uid}")
async def get_item(uid: uuid.UUID, item_service: ItemService = Depends(lambda: get_item_service())) -> Item:
    item = await item_service.get_item(uid)
    if item is None:
        raise HTTPException(status_code=404)
    return item

@router.post("/item")
async def add_item(item_create: ItemCreate, item_service: ItemService = Depends(lambda: get_item_service())) -> Item:
    item = await item_service.add_item(item_create)
    return item

@router.post("/items")
async def add_items(item_create_list: list[ItemCreate], item_service: ItemService = Depends(lambda: get_item_service())):
    items = await item_service.add_items(item_create_list)
    return items

@router.post("/items/get")
async def get_items(item_id_list:  SelectedItems, item_service: ItemService = Depends(lambda: get_item_service())) -> list[Item]:
    item = await item_service.get_items(item_id_list.item_id_list)
    if item is None:
        raise HTTPException(status_code=404)
    return item