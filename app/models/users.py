import uuid

from pydantic import BaseModel, Field
from typing import List, Optional

class User(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    pack_ids: Optional[List[str]] = Field(...)
    
    class Config:
        schema_extra = {
            "example": {
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
