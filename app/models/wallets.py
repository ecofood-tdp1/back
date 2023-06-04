import uuid
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field

from app.models.price import Price


class TransactionOperation(Enum):
    deposit = "deposit"
    withdraw = "withdraw"


class WalletTransaction(Price):
    operation: TransactionOperation


class WalletCreation(BaseModel):
    balance: Price = Field(...)
    transactions: List[WalletTransaction] = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "balance": {
                    "amount": 500,
                    "currency": "ARS",
                },
                "transactions": [
                    {
                        "operation": TransactionOperation.deposit,
                        "amount": 500,
                        "currency": "ARS",
                    }
                ]
            }
        }


class Wallet(WalletCreation):
    shop_id: str = Field(alias="_id")


class WalletUpdate(WalletTransaction):
    class Config:
        schema_extra = {
            "example": {
                "operation": TransactionOperation.deposit,
                "amount": 500,
                "currency": "ARS",
            }
        }
