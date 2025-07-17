import uuid

from src.core.models import Item, ItemCreate
from src.core.ports.abstract_item_repository import AbstractItemRepository


class ItemService:
    """
    A domain service responsible for operations with item.
    """
    def __init__(self, repository: AbstractItemRepository):
        """
        Initiate with a repository.

        :param repository: object implementing AbstractItemRepository
        """
        self.repository = repository

    async def add_item(self, item_create: ItemCreate) -> Item:
        """
        Save an item, generate an id for it and return to the caller.

        :param item_create: data transfer object to create an item
        :return: item domain model
        """
        item = Item(iid=uuid.uuid4(), **item_create.model_dump())
        try:
            await self.repository.save_item(item)
        except Exception as e:
            print(e)
            raise
        return item

    async def get_all_items_by_shop_id(self, shop_id: uuid.UUID) -> list[Item]:
        """
        Get all items that are available in the shop

        :param shop_id: uuid
        :return: list of item domain models
        """
        try:
            return await self.repository.get_all_items_by_shop_id(shop_id)
        except Exception as e:
            print(e)
            raise

    async def add_items(self, item_create_list: list[ItemCreate]) -> list[Item]:
        """
        Save all items from the list into the database.

        :param item_create_list: dtos of items
        :return: list of item domain models
        """
        items = [Item(iid=uuid.uuid4(), **item.model_dump()) for item in item_create_list]
        try:
            await self.repository.save_items(items)
        except Exception as e:
            print(e)
            raise
        return items

    async def get_item(self, item_id: uuid.UUID) -> Item | None:
        """
        Get a particular Item or None by id.

        :param item_id: uuid
        :return: Item if one exists, None otherwise
        """
        try:
            return await self.repository.get_item(item_id)
        except ValueError:
            return None
        except Exception as e:
            print(e)
            raise

    async def get_items(self, item_id_list: list[uuid.UUID]) -> list[Item]:
        """
        Get items with ids in item_id_list.

        :param item_id_list: list of item uids.
        :return: list of item domain objects
        """
        try:
            return await self.repository.get_items(item_id_list)
        except ValueError:
            return None
        except Exception as e:
            print(e)
            raise
