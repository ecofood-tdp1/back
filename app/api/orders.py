from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List, Optional

from app.api.shops import update_wallet
from app.models.orders import Order, OrderUpdateStatus, OrderStatus
from app.models.wallets import WalletUpdate, TransactionOperation

orders_router = APIRouter()


FEE = 0.3


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
def get_orders(request: Request, shop_id: Optional[str] = None, user_id: Optional[str] = None):
    filters = {}
    if shop_id:
        filters["shop_id"] = shop_id
    if user_id:
        filters["user_id"] = user_id

    orders = list(request.app.database["orders"].find(filters, limit=100))
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
    current_order = find_order(id, request)

    if current_order["status"] == OrderStatus.delivered.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Order with ID {id} has already been delivered",
        )

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
        if existing_order["status"] == OrderStatus.delivered.value:
            wallet_update = WalletUpdate(
                amount=float(existing_order["total"]["amount"]) * FEE,
                currency=existing_order["total"]["currency"],
                operation=TransactionOperation.deposit,
            )
            try:
                update_wallet(existing_order["shop_id"], request, wallet_update)
            except HTTPException:
                request.app.logger.error(f"Could not update wallet for shop {existing_order['shop_id']}")

        return existing_order

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Order with ID {id} not found"
    )
