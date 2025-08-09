import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from .database import get_client, get_database
from .schemas import ItemCreate, ItemDB
from .crud import create_item, list_items, get_item, update_item, delete_item

app = FastAPI(title="FastAPI + MongoDB (motor) example")

# Health check endpoint
@app.get('/health')
async def health():
    try:
        client = await get_client()
        info = client.server_info()
        return {"status": "ok", "version": info.get('version')}
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))

@app.post('/items', response_model=ItemDB)
async def api_create_item(item: ItemCreate):
    doc = await create_item(item)
    return doc

@app.get('/items', response_model=List[ItemDB])
async def api_list_items():
    return await list_items()

@app.get('/items/{item_id}', response_model=ItemDB)
async def api_get_item(item_id: str):
    doc = await get_item(item_id)
    if not doc:
        raise HTTPException(status_code=404, detail='Item not found')
    return doc

@app.put('/items/{item_id}', response_model=ItemDB)
async def api_update_item(item_id: str, payload: ItemCreate):
    doc = await update_item(item_id, payload.dict())
    if not doc:
        raise HTTPException(status_code=404, detail='Item not found')
    return doc

@app.delete('/items/{item_id}')
async def api_delete_item(item_id: str):
    await delete_item(item_id)
    return {"status": "deleted"}