import uuid

from src.core.models import Item, ItemCreate
from src.core.ports.abstract_item_repository import AbstractItemRepository


class ItemService:
    def __init__(self, repository: AbstractItemRepository):
        self.repository = repository

    async def add_item(self, item_create: ItemCreate) -> Item:
        item = Item(iid=uuid.uuid4(), **item_create.model_dump())
        try:
            await self.repository.save_item(item)
        except Exception as e:
            print(e)
            raise
        return item

    async def get_all_items_by_shop_id(self, shop_id: uuid.UUID) -> list[Item]:
        try:
            return await self.repository.get_all_items_by_shop_id(shop_id)
        except Exception as e:
            print(e)
            raise

    async def add_items(self, item_create_list: list[Item]) -> list[Item]:
        items = [Item(iid=uuid.uuid4(), **item.model_dump()) for item in item_create_list]
        try:
            await self.repository.save_items(items)
        except Exception as e:
            print(e)
            raise
        return items

    async def get_item(self, item_id: uuid.UUID) -> Item | None:
        try:
            return await self.repository.get_item(item_id)
        except ValueError:
            return None
        except Exception as e:
            print(e)
            raise
