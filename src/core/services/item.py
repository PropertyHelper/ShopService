import uuid

from src.core.models import Item
from src.core.ports.abstract_item_repository import AbstractItemRepository


class ItemService:
    def __init__(self, repository: AbstractItemRepository):
        self.repository = repository

    async def add_item(self, item: Item) -> Item:
        try:
            await self.repository.save_item(item)
        except Exception as e:
            print(e)
            raise
        return item

    async def get_all_items(self) -> list[Item]:
        try:
            return await self.repository.get_all_items()
        except Exception as e:
            print(e)
            raise

    async def add_items(self, items: list[Item]) -> list[Item]:
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
