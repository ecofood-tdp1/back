import uuid
from enum import Enum

from pydantic import BaseModel, Field, validator


class Issuer(Enum):
    visa = 'visa'
    mastercard = 'mastercard'


class MockedCard(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    pan: str = Field(...)
    expiration_date: str = Field(regex=r"(1[0-2]|0[1-9]|\d)/(2[3-9]|[3-9]\d)")
    cardholder_name: str = Field(...)
    issuer: Issuer = Field(default="visa")

    def __eq__(self, other):
        if isinstance(other, MockedCard):
            print(f"equals {self.issuer} == {other.issuer}")
            return self.id == other.id or (
                    self.pan == other.pan and
                    self.expiration_date == other.expiration_date and
                    self.cardholder_name == other.cardholder_name and
                    self.issuer == other.issuer
            )
        return False

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "pan": "4242424242424242",
                "expiration_date": "12/24",
                "cardholder_name": "Lionel Messi",
                "issuer": "visa",
            }
        }


class MockedCardRequestBody(BaseModel):
    expiration_date: str = Field(regex=r"(1[0-2]|0[1-9]|\d)/(2[3-9]|[3-9]\d)")
    cardholder_name: str = Field(...)
    issuer: str = Field(default="visa")

    class Config:
        schema_extra = {
            "example": {
                "expiration_date": "12/24",
                "cardholder_name": "Lionel Messi",
                "issuer": "visa",
            }
        }
