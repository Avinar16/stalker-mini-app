from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from db import AsyncSession
from settings import settings
from schemas import ItemResponse, ItemCreate
from use_cases import create_item, get_item_by_id

app = FastAPI()

# WIP
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.allowed_origins],
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/items/", response_model=ItemResponse)
async def create_item_endpoint(item_: ItemCreate):
    item_data = item_.model_dump()
    created_item = await create_item(item_data)
    return created_item

@app.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int):
    item = await get_item_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item