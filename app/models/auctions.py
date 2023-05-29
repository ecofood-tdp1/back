import uuid
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from app.models.price import Price, Currency
from app.models.shops import ShopType


class AuctionStatus(Enum):
    not_started = "not_started"
    in_progress = "in_progress"
    finished = "finished"


class Auction(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    status: AuctionStatus = Field(default=AuctionStatus.not_started)
    shop_type: str = Field(...)
    bid: Price = Field(...)
    current_winner_id: Optional[str] = None

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "status": "not_started",
                "shop_type": ShopType.restaurant,
                "bid": {
                    "amount": 500,
                    "currency": Currency.USD
                },
                "current_winner_id": "shop_id",
            }
        }


class AuctionUpdate(BaseModel):
    status: Optional[AuctionStatus] = None
    bid: Optional[Price] = None
    current_winner_id: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "status": "not_started",
                "bid": {
                    "amount": 500,
                    "currency": Currency.USD
                },
                "current_winner_id": "shop_id",
            }
        }
