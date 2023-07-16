import uuid
from datetime import datetime
from enum import Enum
from typing import List, Union
from app.models.packs import Pack
from datetime import date, timedelta
from pydantic import BaseModel, Field, validator

from app.models.price import Price


class OrderStatus(Enum):
    paid = "paid"
    marked_as_delivered = "marked_as_delivered"
    delivered = "delivered"


class Order(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    status: OrderStatus = Field(default=OrderStatus.paid)
    user_id: str = Field(...)
    shop_id: str = Field(...)
    # transaction_id: str = Field(...)
    total: Price = Field(...)
    packs: List[Pack] = Field(...)
    created_at: Union[str, datetime] = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "status": "paid",
                "user_id": "4016cb54-ff0e-46a6-ace5-69304d9720c7",
                "shop_id": "e6d09849-c62f-4fbc-9c9a-4e4c8230aa4d",
                "total": {
                    "amount": 2500,
                    "currency": "ARS",
                },
                "packs": [
                    {
                        "_id": "5191cfc9-c3a5-4abb-834b-4ee4e34dd90e",
                        "shop_id": "e6d09849-c62f-4fbc-9c9a-4e4c8230aa4d",
                        "type": "specific",
                        "name": "Docena de empanadas",
                        "description": "Las mejores empanadas de Buenos Aires",
                        "products": [
                            {
                                "name": "Empanada de Carne cortada a cuchillo",
                                "quantity": 4,
                            },
                            {
                                "name": "Empanada de Jamón y Queso",
                                "quantity": 4,
                            },
                            {
                                "name": "Empanada de Pollo",
                                "quantity": 4,
                            },
                        ],
                        "stock": 10,
                        "best_before": (date.today() + timedelta(days=2)).strftime(
                            "%d/%m/%Y"
                        ),
                        "price": {
                            "amount": 2500,
                            "currency": "ARS",
                        },
                        "original_price": {
                            "amount": 4000,
                            "currency": "ARS",
                        },
                        "imageURL": "http://exampleimage.com",
                    }
                ],
                "created_at": datetime.now().strftime("%m/%d/%Y %H:%M:%S"),
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
