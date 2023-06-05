from fastapi import APIRouter

from .auctions import auctions_router
from .mocks import mocks_router
from .orders import orders_router
from .packs import packs_router
from .payments import payments_router
from .shops import shops_router
from .transactions import transactions_router
from .users import users_router
from .ws import ws_router

api_router = APIRouter()


api_router.include_router(shops_router, tags=["Shops"], prefix="/shops")
api_router.include_router(packs_router, tags=["Packs"], prefix="/packs")
# api_router.include_router(transactions_router, tags=["Transactions"], prefix="/transactions")
api_router.include_router(users_router, tags=["Users"], prefix="/users")
api_router.include_router(orders_router, tags=["Orders"], prefix="/orders")
api_router.include_router(auctions_router, tags=["Auctions"], prefix="/auctions")
api_router.include_router(payments_router, tags=["Payments"], prefix="/payments")
api_router.include_router(mocks_router, tags=["Mocks"], prefix="/mocks")
api_router.include_router(ws_router, tags=["Web Socket"], prefix="/ws")
