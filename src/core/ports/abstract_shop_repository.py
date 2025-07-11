from abc import ABC, abstractmethod

from src.core.models import ShopSave, Shop


class AbstractShopRepository(ABC):
    @abstractmethod
    async def save_shop(self, shop: ShopSave) -> Shop:
        ...

    @abstractmethod
    async def get_shop_hashed_password(self, nickname: str) -> str:
        ...

    @abstractmethod
    async def get_shop_by_nickname(self, nickname: str) -> Shop:
        ...
