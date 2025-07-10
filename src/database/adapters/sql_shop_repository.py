from sqlalchemy import select

from src.core.models import ShopCreate, Shop
from src.core.ports.abstract_shop_repository import AbstractShopRepository
from src.database.adapters.sql_base_class import SQLBaseClass
from src.database.models import Shop as ShopModel


class SQLShopRepository(SQLBaseClass, AbstractShopRepository):
    async def save_shop(self, shop_create: ShopCreate) -> Shop:
        async with self.get_session() as session:
            shop_model = ShopModel(sid=shop_create.sid,
                                   password_hash=shop_create.password,
                                   nichname=shop_create.nichname)
            session.add(shop_model)
            await session.commit()
        return Shop(sid=shop_model.sid, nickname=shop_model.nichname)


    async def get_shop_hashed_password(self, nickname: str) -> str:
        async with self.get_session() as session:
            stmt = select(ShopModel.password_hash).where(ShopModel.nichname == nickname)
            result = await session.execute(stmt)
            password = result.scalar_one_or_none()
            if password is None:
                return ""
            return password
