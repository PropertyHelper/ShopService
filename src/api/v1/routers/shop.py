import uuid

from fastapi import APIRouter, Depends, HTTPException

from src.api.v1.dependencies import get_shop_service, get_item_service
from src.api.v1.models import ShopItems, ShopNames
from src.core.models import ShopCreate, ShopLogInRequest, Shop
from src.core.services.item import ItemService
from src.core.services.shop import ShopService

router = APIRouter(prefix="/shop")


@router.post("/")
async def add_shop(shop_create: ShopCreate, shop_service: ShopService = Depends(lambda: get_shop_service())) -> Shop:
    try:
        shop = await shop_service.create_shop(shop_create)
    except ValueError:
        raise HTTPException(status_code=400, detail="nickname already exists")
    return shop


@router.post("/login")
async def login_shop(login_request: ShopLogInRequest, shop_service: ShopService = Depends(lambda: get_shop_service())) -> Shop:
    can_login = await shop_service.shop_can_login(login_request)
    if not can_login:
        raise HTTPException(status_code=403)
    shop = await shop_service.get_shop_by_nickname(login_request.nickname)
    if shop is None:
        # should be impossible
        print(f"Very weird, shop with nickname {login_request.nickname} was able to login, but unable to fetch the username")
        raise HTTPException(status_code=404)
    return shop

@router.get("/{uid}/items")
async def get_items(uid: uuid.UUID, item_service: ItemService = Depends(lambda: get_item_service())) -> ShopItems:
    items = await item_service.get_all_items_by_shop_id(uid)
    return ShopItems(items=items, total=len(items))


@router.post("/names")
async def get_names(shop_id_list: list[uuid.UUID], shop_service: ShopService = Depends(lambda: get_shop_service())) -> ShopNames:
    names = await shop_service.get_names(shop_id_list)
    print(names)
    return ShopNames(names=names)
