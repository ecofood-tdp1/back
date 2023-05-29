from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from app.models.orders import Order, OrderUpdateStatus

orders_router = APIRouter()


@orders_router.post(
    "",
    response_description="Create a new order",
    status_code=status.HTTP_201_CREATED,
    response_model=Order,
)
def create_order(request: Request, order: Order = Body(...)):
    order = jsonable_encoder(order)
    new_order = request.app.database["orders"].insert_one(order)  # joy division (?
    created_order = request.app.database["orders"].find_one(
        {"_id": new_order.inserted_id}
    )

    return created_order


@orders_router.get(
    "", response_description="List all orders", response_model=List[Order]
)
def get_orders(request: Request):
    orders = list(request.app.database["orders"].find(limit=100))
    return orders


@orders_router.get(
    "/{id}", response_description="Get a single order by id", response_model=Order
)
def find_order(id: str, request: Request):
    if (order := request.app.database["orders"].find_one({"_id": id})) is not None:
        return order
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Order with ID {id} not found"
    )


@orders_router.put(
    "/{id}", response_description="Update an order status", response_model=Order
)
def update_order_status(id: str, request: Request, order: OrderUpdateStatus = Body(...)):
    order = {k: v for k, v in order.dict().items() if v is not None}
    if len(order) >= 1:
        update_result = request.app.database["orders"].update_one(
            {"_id": id}, {"$set": jsonable_encoder(order)}
        )

        if update_result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Order with ID {id} not found",
            )

    if (
            existing_order := request.app.database["orders"].find_one({"_id": id})
    ) is not None:
        return existing_order

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Order with ID {id} not found"
    )