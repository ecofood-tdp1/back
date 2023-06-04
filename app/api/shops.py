import re

from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List, Optional
from pymongo import UpdateOne

from app.models.shops import Shop, ShopUpdate
from app.models.wallets import Wallet, WalletUpdate, TransactionOperation, WalletCreation

shops_router = APIRouter()


@shops_router.post(
    "",
    response_description="Create a new shop",
    status_code=status.HTTP_201_CREATED,
    response_model=Shop,
)
def create_shop(request: Request, shop: Shop = Body(...)):
    shop = jsonable_encoder(shop)
    new_shop = request.app.database["shops"].insert_one(shop)
    created_shop = request.app.database["shops"].find_one(
        {"_id": new_shop.inserted_id}
    )

    return created_shop


@shops_router.get(
    "", response_description="List all shops", response_model=List[Shop]
)
def get_shops(request: Request, neighborhood: Optional[str] = None, type: Optional[str] = None):
    filters = {}
    if neighborhood:
        filters["neighborhood"] = re.compile(neighborhood, re.IGNORECASE)

    if type:
        filters["type"] = type

    shops = list(request.app.database["shops"].find(filters, limit=100))
    return shops


@shops_router.get(
    "/{id}", response_description="Get a single shop by id", response_model=Shop
)
def find_shop(id: str, request: Request):
    if (shop := request.app.database["shops"].find_one({"_id": id})) is not None:
        return shop
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Shop with ID {id} not found"
    )


@shops_router.put(
    "/{id}", response_description="Update a shop", response_model=Shop
)
def update_shop(id: str, request: Request, shop: ShopUpdate = Body(...)):
    shop = {k: v for k, v in shop.dict().items() if v is not None}
    if len(shop) >= 1:
        update_result = request.app.database["shops"].update_one(
            {"_id": id}, {"$set": jsonable_encoder(shop)}
        )

        if update_result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Shop with ID {id} not found",
            )

    if (
            existing_shop := request.app.database["shops"].find_one({"_id": id})
    ) is not None:
        return existing_shop

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Shop with ID {id} not found"
    )


@shops_router.delete("/{id}", response_description="Delete a shop")
def delete_shop(id: str, request: Request, response: Response):
    delete_result = request.app.database["shops"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Shop with ID {id} not found"
    )


@shops_router.get("/{id}/wallet", response_description="Get a shop Wallet balance", response_model=Wallet)
def get_shop_wallet(id: str, request: Request):
    if (wallet := request.app.database["wallets"].find_one({"_id": id})) is not None:
        return wallet
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Wallet for shop {id} not found"
    )


@shops_router.post(
    "/{id}/wallet",
    response_description="Create a new wallet",
    status_code=status.HTTP_201_CREATED,
    response_model=Wallet,
)
def create_wallet(id: str, request: Request, wallet: WalletCreation = Body(...)):
    wallet = Wallet(
        shop_id=id,
        balance=wallet.balance,
        transactions=wallet.transactions,
    )
    wallet = jsonable_encoder(wallet)
    print(f"la wallet es {wallet}")
    new_wallet = request.app.database["wallets"].insert_one(wallet)
    print(f"la new wallet es {new_wallet}")
    created_wallet = request.app.database["wallets"].find_one(
        {"_id": new_wallet.inserted_id}
    )

    return created_wallet


@shops_router.put(
    "/{id}/wallet", response_description="Push a transaction into a shop wallet", response_model=Wallet
)
def update_wallet(id: str, request: Request, transaction: WalletUpdate = Body(...)):
    new_amount = transaction.amount
    if transaction.operation == TransactionOperation.withdraw:
        new_amount *= -1

    transaction = {k: v for k, v in transaction.dict().items() if v is not None}
    print(transaction)
    if len(transaction) >= 1:
        update_result = request.app.database["wallets"].bulk_write([
            UpdateOne({"_id": id}, {"$push": {"transactions": jsonable_encoder(transaction)}}, upsert=True),
            UpdateOne({"_id": id}, {"$inc": {"balance.amount": new_amount}}, upsert=True),
        ])

        if update_result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Wallet for shop with ID {id} not found",
            )

    if (
            existing_wallet := request.app.database["wallets"].find_one({"_id": id})
    ) is not None:
        return existing_wallet

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Wallet for shop with ID {id} not found",
    )
