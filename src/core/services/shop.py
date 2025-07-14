import uuid

import bcrypt
from sqlalchemy.exc import IntegrityError

from src.core.models import ShopCreate, Shop, ShopLogInRequest, ShopSave
from src.core.ports.abstract_shop_repository import AbstractShopRepository


class ShopService:
    def __init__(self, repository: AbstractShopRepository):
        self.repository = repository

    async def create_shop(self, create_shop: ShopCreate) -> Shop:
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
        try:
            db_password_hash = await self.repository.get_shop_hashed_password(login_request.nickname.lower())
            if not db_password_hash:
                return False
            return bcrypt.checkpw(login_request.password.encode("utf-8"), db_password_hash.encode("utf-8"))
        except Exception as e:
            print(e)
            raise

    async def get_shop_by_nickname(self, nickname: str) -> Shop | None:
        try:
            shop = await self.repository.get_shop_by_nickname(nickname.lower())
        except ValueError:
            return None
        except Exception as e:
            print(e)
            raise
        return shop

    async def get_names(self, shop_id_list: list[uuid.UUID]) -> list[str]:
        try:
            names = await self.repository.get_names(shop_id_list)
        except Exception as e:
            print(e)
            raise
        return names