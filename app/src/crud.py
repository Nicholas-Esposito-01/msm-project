from typing import List
from .database import get_database
from .schemas import ItemCreate, ItemDB

async def create_item(item: ItemCreate) -> dict:
    db = get_database()
    doc = item.dict()
    res = await db.items.insert_one(doc)
    return await db.items.find_one({"_id": res.inserted_id})

async def list_items() -> List[dict]:
    db = get_database()
    cursor = db.items.find()
    return await cursor.to_list(length=100)

async def get_item(item_id):
    db = get_database()
    from bson import ObjectId
    return await db.items.find_one({"_id": ObjectId(item_id)})

async def update_item(item_id, data: dict):
    db = get_database()
    from bson import ObjectId
    await db.items.update_one({"_id": ObjectId(item_id)}, {"$set": data})
    return await db.items.find_one({"_id": ObjectId(item_id)})

async def delete_item(item_id):
    db = get_database()
    from bson import ObjectId
    await db.items.delete_one({"_id": ObjectId(item_id)})
    return True