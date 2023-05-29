import uuid
from datetime import date, timedelta
from enum import Enum
from typing import Optional, List, Union
from pydantic import BaseModel, Field

from app.models.price import Price


class PackType(Enum):
    surprise = "surprise"
    specific = "specific"


class Product(BaseModel):
    name: str = Field(...)
    quantity: int = Field(..., ge=1)
    best_before: Optional[Union[str, date]] = Field(default=None)


class Pack(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    shop_id: str = Field(...)
    type: PackType = Field(...)
    name: str = Field(...)
    description: Optional[str] = Field(...)
    products: Optional[List[Product]] = Field(...)
    stock: int = Field(..., gt=0)
    best_before: Union[str, date] = Field(...)
    price: Price = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "shop_id": "abc-123",
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
                    }
                ],
                "stock": 10,
                "best_before": (date.today() + timedelta(days=2)).strftime("%d/%m/%Y"),
                "price": {
                    "amount": 2500,
                    "currency": "ARS",
                }
            }
        }


class PackUpdate(BaseModel):
    name: Optional[str] = Field(...)
    description: Optional[str] = Field(...)
    products: Optional[List[Product]] = Field(...)
    stock: Optional[int] = Field(..., gt=0)
    best_before: Union[str, date, None] = Field(...)
    price: Optional[Price] = Field(...)

    class Config:
        schema_extra = {
            "example": {
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
                    }
                ],
                "stock": 10,
                "best_before": (date.today() + timedelta(days=2)).strftime("%d/%m/%Y"),
                "price": {
                    "amount": 2500,
                    "currency": "ARS",
                }
            }
        }
