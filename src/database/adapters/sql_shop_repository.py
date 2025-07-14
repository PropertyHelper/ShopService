import uuid

from sqlalchemy import select

from src.core.models import ShopSave, Shop
from src.core.ports.abstract_shop_repository import AbstractShopRepository
from src.database.adapters.sql_base_class import SQLBaseClass
from src.database.models import Shop as ShopModel


class SQLShopRepository(SQLBaseClass, AbstractShopRepository):
    async def save_shop(self, shop_create: ShopSave) -> Shop:
        async with self.get_session() as session:
            shop_model = ShopModel(sid=shop_create.sid,
                                   password_hash=shop_create.password,
                                   nickname=shop_create.nickname)
            session.add(shop_model)
            await session.commit()
        return Shop(sid=shop_model.sid, nickname=shop_model.nickname)


    async def get_shop_hashed_password(self, nickname: str) -> str:
        async with self.get_session() as session:
            stmt = select(ShopModel.password_hash).where(ShopModel.nickname == nickname)
            result = await session.execute(stmt)
            password = result.scalar_one_or_none()
            if password is None:
                return ""
            return password

    async def get_shop_by_nickname(self, nickname: str) -> Shop:
        async with self.get_session() as session:
            stmt = select(ShopModel).where(ShopModel.nickname == nickname)
            result = await session.execute(stmt)
            shop_model = result.scalar_one_or_none()
            if shop_model is None:
                raise ValueError(f"No shop with nickname {nickname}")
            return Shop(
                sid=shop_model.sid,
                nickname=shop_model.nickname
            )

    async def get_names(self, shop_id_list: list[uuid.UUID]) -> list[str]:
        async with self.get_session() as session:
            stmt = select(ShopModel.sid, ShopModel.nickname).where(ShopModel.sid.in_(shop_id_list))
            result = await session.execute(stmt)
            sid_to_name = {sid: name for sid, name in result.all()}
            return [sid_to_name.get(sid, "") for sid in shop_id_list]
