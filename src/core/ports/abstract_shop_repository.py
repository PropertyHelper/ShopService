import uuid
from abc import ABC, abstractmethod

from src.core.models import ShopSave, Shop


class AbstractShopRepository(ABC):
    """
    Abstract interface for any shop repository infrastructure.
    """
    @abstractmethod
    async def save_shop(self, shop: ShopSave) -> Shop:
        """
        Save the shop into the infrastructure.

        :param shop: shop save model
        :return: shop domain model
        """
        ...

    @abstractmethod
    async def get_shop_hashed_password(self, nickname: str) -> str:
        """
        Get the shop password

        :param nickname: shop unique name
        :return: password hash
        """
        ...

    @abstractmethod
    async def get_shop_by_nickname(self, nickname: str) -> Shop:
        """
        Get shop from infrastructure

        :param nickname: shop unique name
        :return: shop domain model
        """
        ...

    @abstractmethod
    async def get_names(self, shop_id_list: list[uuid.UUID]) -> list[str]:
        """
        Get list of shop names by shop ids

        :param shop_id_list: list of ids of shops
        :return: list of shop names
        """
        ...