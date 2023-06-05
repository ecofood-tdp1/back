import uuid
from enum import Enum

from pydantic import BaseModel, Field

from app.models.price import Price


class Issuer(Enum):
    visa = 'visa'
    mastercard = 'mastercard'


class PaymentType(Enum):
    card = 'card'


class PaymentTransaction(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    type: PaymentType = Field(default="card")
    user_id: str = Field(...)
    last_numbers: str = Field(...)
    issuer: Issuer = Field(default="visa")
    total: Price = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "type": "card",
                "user_id": "d8f7ecd5-f8b6-4a68-a5c1-31d7300cda26",
                "last_numbers": "1234",
                "issuer": "visa",
                "total": {
                    "amount": 2500,
                    "currency": "ARS",
                }
            }
        }


class EncryptedPaymentMethodBody(BaseModel):
    pan: str = Field(...)
    cardholder_name: str = Field(...)
    expiration_date: str = Field(...)
    issuer: str = Field(...)


class TransactionBody(BaseModel):
    user_id: str = Field(...)
    payment_method: EncryptedPaymentMethodBody = Field(...)
    total: Price = Field(default=None)

    class Config:
        schema_extra = {
            "example": {
                "user_id": "abc-123",
                "payment_method": {
                    "pan": "",
                    "cardholder_name": "",
                    "expiration_date": "",
                    "issuer": "",
                },
                "total": {
                    "amount": 2500,
                    "currency": "ARS",
                },
            }
        }
