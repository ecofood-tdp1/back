from fastapi import APIRouter, Body, Request, status, Header, HTTPException
from fastapi.encoders import jsonable_encoder

from typing import Union

from app.models.users import User, UserUpdate, AppendPackIds


users_router = APIRouter()

@users_router.post(
    "",
    response_description="Create a new user",
    status_code=status.HTTP_201_CREATED,
    response_model=User,
)
def create_user(request: Request, user: User = Body(...)):
    user = jsonable_encoder(user)
    new_user = request.app.database["users"].insert_one(user)
    created_user = request.app.database["users"].find_one(
        {"_id": new_user.inserted_id}
    )

    return created_user

@users_router.put(
    "",
    response_description="Update user",
    response_model=User,
)
def update_user(request: Request, x_user_id: Union[str, None] = Header(default=None), user_update: UserUpdate = Body(...)):
    
    update_result = request.app.database["users"].update_one(
            {"_id": x_user_id}, {"$set": jsonable_encoder(user_update)}
        )
    if update_result.matched_count == 0:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {x_user_id} not found",
            )
    user = request.app.database["users"].find_one(
        {"_id": x_user_id}
    )
    return user

@users_router.get(
    "",
    response_description="Get User",
    response_model=User,
)
def add_to_cart(request: Request, x_user_id: Union[str, None] = Header(default=None)):
    user = request.app.database["users"].find_one(
        {"_id": x_user_id}
    )
    if user is None:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {x_user_id} not found",
            )
    return user

@users_router.patch(
    "/shopcart",
    response_description="Add to shop cart",
    response_model=User,
)
def add_to_cart(request: Request, x_user_id: Union[str, None] = Header(default=None), append_pack_ids: AppendPackIds = Body(...)):
    user = request.app.database["users"].find_one(
        {"_id": x_user_id}
    )
    if user is None:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {x_user_id} not found",
            )
    searched_packs = request.app.database["packs"].count_documents({"_id": {"$in": append_pack_ids.pack_ids}})
    print(searched_packs)
    if searched_packs != len(append_pack_ids.pack_ids):
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Not every pack id could be found",
            )
    user["pack_ids"].extend(append_pack_ids.pack_ids)
    request.app.database["users"].update_one(
            {"_id": user["_id"]}, {"$set": user}
        )

    return user

@users_router.delete(
    "/shopcart/{pack_id}",
    response_description="Add to shop cart",
)
def add_to_cart(pack_id: str, request: Request, x_user_id: Union[str, None] = Header(default=None)):
    user = request.app.database["users"].find_one(
        {"_id": x_user_id}
    )
    if user is None:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {x_user_id} not found",
            )
    try:
        user["pack_ids"].remove(pack_id)
    except ValueError:
        pass
    request.app.database["users"].update_one(
            {"_id": user["_id"]}, {"$set": user}
        )
    return