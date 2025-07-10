from abc import ABC, abstractmethod

from src.core.models import ShopCreate, Shop


class AbstractShopRepository(ABC):
    @abstractmethod
    async def save_shop(self, shop: ShopCreate) -> Shop:
        ...

    @abstractmethod
    async def get_shop_hashed_password(self, nickname: str) -> str:
        ...
