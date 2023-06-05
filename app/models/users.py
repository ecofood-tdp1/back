import uuid
from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional

class UserType(Enum):
    buyer = "buyer"
    shop = "shop"


class User(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    type: UserType = Field(...)
    display_name: str = Field(...)
    pack_ids: Optional[List[str]] = Field(...)
    
    class Config:
        schema_extra = {
            "example": {
                "type": "buyer",
                "display_name": "Lionel Messi",
                "pack_ids": [
                    "89128j1982d12"
                ]
            }
        }

class UserUpdate(BaseModel):
    pack_ids: Optional[List[str]] = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "pack_ids": [
                    "89128j1982d12"
                ]
            }
        }

class AppendPackIds(BaseModel):
    pack_ids: Optional[List[str]] = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "pack_ids": [
                    "89128j1982d12"
                ]
            }
        }
