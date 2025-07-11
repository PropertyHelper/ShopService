from fastapi import APIRouter, Depends, HTTPException

from src.api.v1.dependencies import get_cashier_service
from src.core.models import CashierLoginRequest, CashierCreate, Cashier
from src.core.services.cashier import CashierService

router = APIRouter(prefix="/cashier")

@router.post("/login")
async def login_cashier(login_request: CashierLoginRequest, cashier_service: CashierService = Depends(lambda: get_cashier_service())) -> Cashier:
    can_login = await cashier_service.cashier_can_login(login_request)
    if not can_login:
        raise HTTPException(status_code=403)
    cashier = await cashier_service.get_cashier_by_account_and_shop(login_request.account_name,
                                                                    login_request.shop_nickname)
    return cashier



@router.post("/")
async def add_cashier(cashier_create: CashierCreate, cashier_service: CashierService = Depends(lambda: get_cashier_service())) -> Cashier:
    try:
        cashier = await cashier_service.create_cashier(cashier_create)
    except ValueError:
        raise HTTPException(status_code=400, detail="account already exists")
    return cashier
