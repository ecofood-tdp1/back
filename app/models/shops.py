import uuid
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class ShopType(Enum):
    supermarket = "supermarket"
    bakery = "bakery"
    delicatessen = "delicatessen"
    restaurant = "restaurant"
    coffee = "coffee"
    grocery = "grocery"
    others = "others"


class Shop(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)
    type: ShopType = Field(...)
    pick_up_from: int = Field(...)
    pick_up_to: int = Field(...)
    phone: str = Field(...)
    description: Optional[str] = Field(...)
    address: str = Field(...)
    neighborhood: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "name": "La Continental",
                "type": "restaurant",
                "pick_up_from": 18,
                "pick_up_to": 21,
                "description": "La mejor Pizza de Buenos Aires",
                "phone": "1111-1111",
                "address": "Av. Corrientes 1200",
                "neighborhood": "Balvanera",
            }
        }


class ShopUpdate(BaseModel):
    name: Optional[str] = Field(...)
    type: Optional[ShopType] = Field(...)
    pick_up_from: Optional[int] = Field(...)
    pick_up_to: Optional[int] = Field(...)
    phone: Optional[str] = Field(...)
    description: Optional[str] = Field(...)
    address: Optional[str] = Field(...)
    neighborhood: Optional[str] = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "name": "La Continental",
                "type": "restaurant",
                "pick_up_from": 18,
                "pick_up_to": 21,
                "description": "La mejor Pizza de Buenos Aires",
                "phone": "1111-1111",
                "address": "Av. Corrientes 1200",
                "neighborhood": "Balvanera",
            }
        }
