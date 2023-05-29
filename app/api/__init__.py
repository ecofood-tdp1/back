from fastapi import APIRouter
from .shops import shops_router


api_router = APIRouter()


api_router.include_router(shops_router, tags=["Shops"], prefix="/shops")
