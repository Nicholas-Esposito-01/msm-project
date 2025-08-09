from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

# Helper per Pydantic + ObjectId
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId')
        return ObjectId(v)

class ItemBase(BaseModel):
    name: str = Field(..., min_length=1)
    value: float

class ItemCreate(ItemBase):
    pass

class ItemDB(ItemBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}