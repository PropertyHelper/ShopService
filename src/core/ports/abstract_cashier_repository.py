import uuid
from abc import ABC, abstractmethod

from src.core.models import CashierSave, Cashier


class AbstractCashierRepository(ABC):
    @abstractmethod
    async def save_cashier(self, cashier: CashierSave) -> Cashier:
        ...

    @abstractmethod
    async def get_password_hash(self, shop_nickname: str, account_name: str):
        ...

    @abstractmethod
    async def get_created_cashier_names(self, shop_id: uuid.UUID) -> list[str]:
        ...

    @abstractmethod
    async def get_cashier_by_account_and_shop(self, account_name: str, shop_nickname: str) -> Cashier:
        ...