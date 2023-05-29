import uuid
from datetime import datetime
from enum import Enum
from typing import List, Union

from pydantic import BaseModel, Field


class OrderStatus(Enum):
    paid = "paid"
    marked_as_delivered = "marked_as_delivered"
    delivered = "delivered"


class Order(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    status: OrderStatus = Field(default=OrderStatus.paid)
    user_id: str = Field(...)
    shop_id: str = Field(...)
    transaction_id: str = Field(...)
    products_ids: List[str] = Field(...)
    created_at: Union[str, datetime] = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "status": "paid",
                "user_id": "user-id",
                "shop_id": "shop-id",
                "transaction_id": "transaction_id",
                "products_ids": [
                    "product_1_id",
                    "product_2_id",
                ],
                "created_at": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            }
        }


class OrderUpdateStatus(BaseModel):
    status: OrderStatus = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "status": "delivered",
            }
        }
