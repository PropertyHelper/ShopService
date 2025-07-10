import uuid
from abc import ABC, abstractmethod

from src.core.models import Item

class AbstractItemRepository(ABC):
    @abstractmethod
    async def save_item(self, item: Item) -> None:
        ...

    @abstractmethod
    async def get_all_items(self) -> list[Item]:
        ...

    @abstractmethod
    async def get_item(self, item_id: uuid.UUID) -> Item:
        ...

    @abstractmethod
    async def save_items(self, items: list[Item]) -> None:
        ...
