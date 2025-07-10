import bcrypt

from src.core.models import CashierCreate, Cashier, CashierLoginRequest
from src.core.ports.abstract_cashier_repository import AbstractCashierRepository


class CashierService:
    def __init__(self, repository: AbstractCashierRepository):
        self.repository = repository

    async def create_cashier(self, create_cashier: CashierCreate) -> Cashier:
        created_accounts = self.repository.get_created_cashier_names(create_cashier.shop_id)
        if create_cashier.account_name in created_accounts:
            raise ValueError("Account already exists")
        try:
            password_hash = bcrypt.hashpw(create_cashier.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
            create_cashier.password = password_hash
            cashier = await self.repository.save_cashier(create_cashier)
            return cashier
        except Exception as e:
            print(e)
            raise

    async def cashier_can_login(self, login_request: CashierLoginRequest) -> bool:
        try:
            db_password_hash = await self.repository.get_password_hash(login_request.shop_nickname,
                                                                       login_request.account_name)
            if not db_password_hash:
                return False
            return bcrypt.checkpw(login_request.password.encode("utf-8"), db_password_hash.encode("utf-8"))
        except Exception as e:
            print(e)
            raise
