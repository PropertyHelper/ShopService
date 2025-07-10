import bcrypt
from sqlalchemy.exc import IntegrityError

from src.core.models import ShopCreate, Shop, ShopLogInRequest
from src.core.ports.abstract_shop_repository import AbstractShopRepository


class ShopService:
    def __init__(self, repository: AbstractShopRepository):
        self.repository = repository

    async def create_shop(self, create_shop: ShopCreate) -> Shop:
        try:
            password_hash = bcrypt.hashpw(create_shop.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
            create_shop.password = password_hash
            shop = await self.repository.save_shop(create_shop)
            return shop
        except IntegrityError:
            raise ValueError(f"Given shoop nickname already exist in the system.")
        except Exception as e:
            print(e)
            raise

    async def shop_can_login(self, login_request: ShopLogInRequest) -> bool:
        try:
            db_password_hash = await self.repository.get_shop_hashed_password(login_request.nickname)
            if not db_password_hash:
                return False
            return bcrypt.checkpw(login_request.password.encode("utf-8"), db_password_hash.encode("utf-8"))
        except Exception as e:
            print(e)
            raise
