import uuid

from sqlalchemy import select

from src.core.models import CashierSave, Cashier
from src.core.ports.abstract_cashier_repository import AbstractCashierRepository
from src.database.adapters.sql_base_class import SQLBaseClass
from src.database.models import Cashier as CashierModel, Shop as ShopModel


class SQLCashierRepository(SQLBaseClass, AbstractCashierRepository):
    async def save_cashier(self, cashier_to_save: CashierSave) -> Cashier:
        async with self.get_session() as session:
            cashier_model = CashierModel(cid=cashier_to_save.cid, password_hash=cashier_to_save.password,
                                         account_name=cashier_to_save.account_name, shop_id=cashier_to_save.shop_id)
            session.add(cashier_model)
            await session.commit()
        return Cashier(cid=cashier_model.cid,
                       account_name=cashier_model.account_name,
                       shop_id=cashier_model.shop_id)

    async def get_password_hash(self, shop_nickname: str, account_name: str):
        async with self.get_session() as session:
            stmt = select(CashierModel.password_hash)\
                .where(CashierModel.account_name == account_name)\
                .join(ShopModel, ShopModel.sid == CashierModel.shop_id)\
                .where(ShopModel.nickname == shop_nickname)
            result = await session.execute(stmt)
            password = result.scalar_one_or_none()
            if password is None:
                return ""
            return password

    async def get_created_cashier_names(self, shop_id: uuid.UUID) -> list[str]:
        async with self.get_session() as session:
            stmt = select(CashierModel.account_name).where(CashierModel.shop_id == shop_id)
            result = await session.execute(stmt)
            accounts = [account for account in result.scalars().all()]
            return accounts

    async def get_cashier_by_account_and_shop(self, account_name: str, shop_nickname: str) -> Cashier:
        async with self.get_session() as session:
            stmt = select(CashierModel) \
                .where(CashierModel.account_name == account_name) \
                .join(ShopModel) \
                .where(ShopModel.nickname == shop_nickname)
            result = await session.execute(stmt)
            cashier_model = result.scalar_one_or_none()
            if cashier_model is None:
                raise ValueError("No cashier found")
            return Cashier(cid=cashier_model.cid, account_name=cashier_model.account_name, shop_id=cashier_model.shop_id)
