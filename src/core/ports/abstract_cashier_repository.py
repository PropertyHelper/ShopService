import uuid
from abc import ABC, abstractmethod

from src.core.models import CashierSave, Cashier


class AbstractCashierRepository(ABC):
    """
    Abstract interface for any cashier repository infrastructure.
    """
    @abstractmethod
    async def save_cashier(self, cashier: CashierSave) -> Cashier:
        """
        Save cashier in the infrastructure
        :param cashier: cashier save model
        :return: cashier domain model
        """
        ...

    @abstractmethod
    async def get_password_hash(self, shop_nickname: str, account_name: str) -> str:
        """
        Get cashier's password hash
        :param shop_nickname: shop unique name
        :param account_name: cashier unique (within shop) account name
        :return: hashed password
        """
        ...

    @abstractmethod
    async def get_created_cashier_names(self, shop_id: uuid.UUID) -> list[str]:
        """
        Get cashier names of the shop.

        :param shop_id: uuid
        :return: list of cashier account names
        """
        ...

    @abstractmethod
    async def get_cashier_by_account_and_shop(self, account_name: str, shop_nickname: str) -> Cashier:
        """
        Get cashier based on the shop and account.

        :param account_name: unique within a shop cashier name
        :param shop_nickname: unique shop name
        :return: cashier domain model
        """
        ...