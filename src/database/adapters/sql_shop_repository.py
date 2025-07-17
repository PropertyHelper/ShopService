import uuid

from sqlalchemy import select

from src.core.models import ShopSave, Shop
from src.core.ports.abstract_shop_repository import AbstractShopRepository
from src.database.adapters.sql_base_class import SQLBaseClass
from src.database.models import Shop as ShopModel


class SQLShopRepository(SQLBaseClass, AbstractShopRepository):
    """
    A repository to interact with infrastructure.

    In our case, it interacts with PostgreSQL via SQLAlchemy.
    Implements the AbstractShopRepository contract.
    Subclasses the SQLBaseClass to get basic things like getting a connection.
    """
    async def save_shop(self, shop_create: ShopSave) -> Shop:
        """
        Save shop in the database from dto and get the domain model

        :param shop_create: data transfer object with generated id.
        :return: domain value of shop
        """
        async with self.get_session() as session:
            shop_model = ShopModel(sid=shop_create.sid,
                                   password_hash=shop_create.password,
                                   nickname=shop_create.nickname)
            session.add(shop_model)
            await session.commit()
        return Shop(sid=shop_model.sid, nickname=shop_model.nickname)


    async def get_shop_hashed_password(self, nickname: str) -> str:
        """
        Get the shop management password hash by nickname to compare later.

        :param nickname: shop unique nick name
        :return: either hash, or empty string if nickname is not found
        """
        async with self.get_session() as session:
            stmt = select(ShopModel.password_hash).where(ShopModel.nickname == nickname)
            result = await session.execute(stmt)
            password = result.scalar_one_or_none()
            if password is None:
                return ""
            return password

    async def get_shop_by_nickname(self, nickname: str) -> Shop:
        """
        Get domain model of shop from the database by nickname.

        :param nickname: shop unique nick name
        :return: shop domain model
        :raise ValueError if the shop does not exist
        """
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
        """
        Get list of shop names by a list of uuid's.

        Rules:
         - If the uuid is met multiple times, each time the name is put.
         - If the uuid provided does not correspond to a shop, empty string is inserted.

        :param shop_id_list: list of shop id's
        :return: list of shop names
        """
        async with self.get_session() as session:
            stmt = select(ShopModel.sid, ShopModel.nickname).where(ShopModel.sid.in_(shop_id_list))
            result = await session.execute(stmt)
            sid_to_name = {sid: name for sid, name in result.all()}
            return [sid_to_name.get(sid, "") for sid in shop_id_list]
