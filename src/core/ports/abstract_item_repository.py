import uuid
from abc import ABC, abstractmethod

from src.core.models import Item

class AbstractItemRepository(ABC):
    """
    Abstract interface for any item repository infrastructure.
    """
    @abstractmethod
    async def save_item(self, item: Item) -> None:
        """
        Save item into infrastructure

        :param item: item cre
        :return: None
        """
        ...

    @abstractmethod
    async def get_all_items_by_shop_id(self, shop_id: uuid.UUID) -> list[Item]:
        """
        Get shop items.

        :param shop_id: uuid
        :return: list of domain items
        """
        ...

    @abstractmethod
    async def get_item(self, item_id: uuid.UUID) -> Item:
        """
        Get an item by its id.

        :param item_id: uuid
        :return: item domain model
        """
        ...

    @abstractmethod
    async def save_items(self, items: list[Item]) -> None:
        """
        Save multiple items.

        :param items: list of item models
        :return: None
        """
        ...

    @abstractmethod
    async def get_items(self, item_id_list: list[uuid.UUID]) -> list[Item]:
        """
        Get multiple items with ids specified in the item_id_list.

        :param item_id_list: list of items uuids
        :return: list of domain item models
        """
        ...