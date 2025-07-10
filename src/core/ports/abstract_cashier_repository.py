import uuid
from abc import ABC, abstractmethod

from src.core.models import CashierCreate, Cashier


class AbstractCashierRepository(ABC):
    @abstractmethod
    async def save_cashier(self, cashier: CashierCreate) -> Cashier:
        ...

    @abstractmethod
    async def get_password_hash(self, shop_nickname: str, account_name: str):
        ...

    @abstractmethod
    async def get_created_cashier_names(self, shop_id: uuid.UUID) -> list[str]:
        ...
