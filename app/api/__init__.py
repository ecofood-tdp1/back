from fastapi import APIRouter

from .orders import orders_router
from .packs import packs_router
from .shops import shops_router
from .transactions import transactions_router

api_router = APIRouter()


api_router.include_router(shops_router, tags=["Shops"], prefix="/shops")
api_router.include_router(packs_router, tags=["Packs"], prefix="/packs")
api_router.include_router(transactions_router, tags=["Transactions"], prefix="/transactions")
api_router.include_router(orders_router, tags=["Orders"], prefix="/orders")
