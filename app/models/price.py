from enum import Enum

from pydantic import BaseModel, Field


class Currency(Enum):
    ARS = 'ARS'
    USD = 'USD'


class Price(BaseModel):
    amount: float = Field(..., gt=0)
    currency: Currency = Field(...)
