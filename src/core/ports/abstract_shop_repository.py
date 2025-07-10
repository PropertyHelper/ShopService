from abc import ABC, abstractmethod

from src.core.models import ShopCreate


class AbstractShopRepository(ABC):
    @abstractmethod
    async def save_shop(self, shop: ShopCreate) -> None:
        ...

    @abstractmethod
    async def get_shop_hashed_password(self, nickname: str) -> str:
        ...
