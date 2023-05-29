from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List, Optional

from app.models.packs import Pack, PackUpdate

packs_router = APIRouter()


@packs_router.post(
    "",
    response_description="Create a new pack",
    status_code=status.HTTP_201_CREATED,
    response_model=Pack,
)
def create_pack(request: Request, pack: Pack = Body(...)):
    pack = jsonable_encoder(pack)
    new_pack = request.app.database["packs"].insert_one(pack)
    created_pack = request.app.database["packs"].find_one(
        {"_id": new_pack.inserted_id}
    )

    return created_pack


@packs_router.get(
    "", response_description="List all packs", response_model=List[Pack]
)
def get_packs(request: Request, shop_id: Optional[str] = None):
    filters = {}
    if shop_id:
        filters["shop_id"] = shop_id

    packs = list(request.app.database["packs"].find(filters, limit=100))
    return packs


@packs_router.get(
    "/{id}", response_description="Get a single pack by id", response_model=Pack
)
def get_pack(id: str, request: Request):
    if (pack := request.app.database["packs"].find_one({"_id": id})) is not None:
        return pack
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Pack with ID {id} not found"
    )


@packs_router.put(
    "/{id}", response_description="Update a pack", response_model=Pack
)
def update_pack(id: str, request: Request, pack: PackUpdate = Body(...)):
    pack = {k: v for k, v in pack.dict().items() if v is not None}
    if len(pack) >= 1:
        update_result = request.app.database["packs"].update_one(
            {"_id": id}, {"$set": jsonable_encoder(pack)}
        )

        if update_result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pack with ID {id} not found",
            )

    if (
            existing_pack := request.app.database["packs"].find_one({"_id": id})
    ) is not None:
        return existing_pack

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Pack with ID {id} not found"
    )


@packs_router.delete("/{id}", response_description="Delete a pack")
def delete_pack(id: str, request: Request, response: Response):
    delete_result = request.app.database["packs"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Pack with ID {id} not found"
    )
