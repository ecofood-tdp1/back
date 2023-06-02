import re

from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List, Optional

from app.models.shops import Shop, ShopUpdate

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
