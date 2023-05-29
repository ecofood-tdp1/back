import uuid
from datetime import datetime
from enum import Enum
from typing import Union

from pydantic import BaseModel, Field

from app.models.price import Price


class TransactionStatus(Enum):
    approved = "approved"
    declined = "declined"


class PaymentMethod(Enum):
    MercadoPago = "MercadoPago"


class Transaction(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    status: TransactionStatus = Field(...)
    method: PaymentMethod = Field(default=PaymentMethod.MercadoPago)
    total: Price = Field(...)
    created_at: Union[str, datetime] = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "status": "approved",
                "method": PaymentMethod.MercadoPago,
                "total": {
                    "amount": 2500,
                    "currency": "ARS",
                },
                "created_at": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            }
        }
