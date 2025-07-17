import uuid

import bcrypt

from src.core.models import CashierCreate, Cashier, CashierLoginRequest, CashierSave
from src.core.ports.abstract_cashier_repository import AbstractCashierRepository


class CashierService:
    """
    A domain service responsible for operations with item.
    """
    def __init__(self, repository: AbstractCashierRepository):
        """
        Initiate with a repository.

        :param repository: object implementing AbstractShopRepository
        """
        self.repository = repository

    async def create_cashier(self, create_cashier: CashierCreate) -> Cashier:
        """
        Save a cashier into the storage, allocating an id for it.
        :param create_cashier: dto representing user inputted cashier data
        :return: cashier domain model
        """
        created_accounts = await self.repository.get_created_cashier_names(create_cashier.shop_id)
        if create_cashier.account_name.lower() in [created_account.lower() for created_account in created_accounts]:
            raise ValueError("Account already exists")
        try:
            password_hash = bcrypt.hashpw(create_cashier.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
            cashier_to_save = CashierSave(account_name=create_cashier.account_name.lower(),
                                          shop_id=create_cashier.shop_id,
                                          password=password_hash,
                                          cid=uuid.uuid4())
            cashier = await self.repository.save_cashier(cashier_to_save)
            return cashier
        except Exception as e:
            print(e)
            raise

    async def cashier_can_login(self, login_request: CashierLoginRequest) -> bool:
        """
        Get the answer if a cashier can login
        :param login_request: credentials
        :return: bool whether cashier can log in
        """
        try:
            db_password_hash = await self.repository.get_password_hash(login_request.shop_nickname.lower(),
                                                                       login_request.account_name.lower())
            if not db_password_hash:
                return False
            # compare hash of db password and provided password
            return bcrypt.checkpw(login_request.password.encode("utf-8"), db_password_hash.encode("utf-8"))
        except Exception as e:
            print(e)
            raise

    async def get_cashier_by_account_and_shop(self, account_name: str, shop_nickname: str) -> Cashier | None:
        """
        Get the cashier/None by shop nickname and an account name.
        :param account_name: unique within a shop cashier account
        :param shop_nickname: unique shop name
        :return: cashier domain model
        """
        try:
            shop = await self.repository.get_cashier_by_account_and_shop(account_name.lower(), shop_nickname.lower())
        except ValueError:
            return None
        except Exception as e:
            print(e)
            raise
        return shop
