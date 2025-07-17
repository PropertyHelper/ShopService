import uuid

import bcrypt
from sqlalchemy.exc import IntegrityError

from src.core.models import Shop, ShopLogInRequest, ShopSave
from src.core.ports.abstract_shop_repository import AbstractShopRepository


class ShopService:
    """
    A domain service responsible for operations with shop.
    """
    def __init__(self, repository: AbstractShopRepository):
        """
        Initiate with a repository.

        :param repository: object implementing AbstractShopRepository
        """
        self.repository = repository

    async def create_shop(self, create_shop: ShopSave) -> Shop:
        """
        Get a request to create a shop, allocate uuid and save.

        :param create_shop: data transfer object with shop details provided by user
        :return: shop domain object already saved in the database.
        :raise ValueError if the shop nickname already registered
        """
        try:
            password_hash = bcrypt.hashpw(create_shop.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
            shop_to_save = ShopSave(sid=uuid.uuid4(), nickname=create_shop.nickname.lower(), password=password_hash)
            shop = await self.repository.save_shop(shop_to_save)
            return shop
        except IntegrityError:
            raise ValueError(f"Given shoop nickname already exist in the system.")
        except Exception as e:
            print(e)
            raise

    async def shop_can_login(self, login_request: ShopLogInRequest) -> bool:
        """
        Check if the shop with login_request data is eligible to login.

        :param login_request: model capturing shop credentials
        :return: bool whether the shop can login.
        """
        try:
            db_password_hash = await self.repository.get_shop_hashed_password(login_request.nickname.lower())
            if not db_password_hash:
                return False
            return bcrypt.checkpw(login_request.password.encode("utf-8"), db_password_hash.encode("utf-8"))
        except Exception as e:
            print(e)
            raise

    async def get_shop_by_nickname(self, nickname: str) -> Shop | None:
        """
        Get shop or None by providing nickname

        :param nickname: unique shop name
        :return: shop domain model or None if the shop does not exist
        """
        try:
            shop = await self.repository.get_shop_by_nickname(nickname.lower())
        except ValueError:
            return None
        except Exception as e:
            print(e)
            raise
        return shop

    async def get_names(self, shop_id_list: list[uuid.UUID]) -> list[str]:
        """
        Get shop names by list of uids.

        :param shop_id_list: list of shop uids.
        :return: list of shop names.
        """
        try:
            names = await self.repository.get_names(shop_id_list)
        except Exception as e:
            print(e)
            raise
        return names