from dependency_injector.wiring import Provide, inject

from src.container import Container
from src.core.ports.abstract_cashier_repository import AbstractCashierRepository
from src.core.ports.abstract_item_repository import AbstractItemRepository
from src.core.ports.abstract_shop_repository import AbstractShopRepository
from src.core.services.cashier import CashierService
from src.core.services.item import ItemService
from src.core.services.shop import ShopService


@inject
def get_shop_service(shop_repository: AbstractShopRepository = Provide[Container.shop_repository]) -> ShopService:
    """
    Use to get the shop service.

    :param shop_repository: repository from container DI
    :return: shop service
    Note:
        - used by fastapi DI system
        - uses DI to inject shop_repository in the building process
    """
    return ShopService(repository=shop_repository)


@inject
def get_cashier_service(cashier_repository: AbstractCashierRepository = Provide[Container.cashier_repository]) -> CashierService:
    """
    Use to get the cashier service.

    :param cashier_repository: repository from container DI
    :return: cashier service
    Note:
        - used by fastapi DI system
        - uses DI to inject cashier_repository in the building process
    """
    return CashierService(repository=cashier_repository)


@inject
def get_item_service(item_repository: AbstractItemRepository = Provide[Container.item_repository]) -> ItemService:
    """
    Use to get the item service.

    :param item_repository: repository from container DI
    :return: item service
    Note:
        - used by fastapi DI system
        - uses DI to inject item_repository in the building process
    """
    return ItemService(repository=item_repository)
