from fastapi import APIRouter

from .packs import packs_router
from .shops import shops_router


api_router = APIRouter()


api_router.include_router(shops_router, tags=["Shops"], prefix="/shops")
api_router.include_router(packs_router, tags=["Packs"], prefix="/packs")
