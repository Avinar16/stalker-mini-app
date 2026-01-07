from fastapi import Depends
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.sql.annotation import Annotated

from db import AsyncSession, get_session, AsyncSessionLocal
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from models import Item, Weapon, Armor, Artifact, Backpack, Pistol, Inventory, InventoryItem
from schemas import WeaponCreate, ArmorCreate, ArtifactCreate, BackpackCreate, PistolCreate, ItemBase


async def create_item(item_data: dict):
    session = AsyncSessionLocal
    item_type = item_data.get("type")
    if item_type == "weapon":
        validated_data = WeaponCreate(**item_data).model_dump()
        item = Weapon(**validated_data)
    elif item_type == "armor":
        validated_data = ArmorCreate(**item_data).model_dump()
        item = Armor(**validated_data)
    elif item_type == "artifact":
        validated_data = ArtifactCreate(**item_data).model_dump()
        item = Artifact(**validated_data)
    elif item_type == "backpack":
        validated_data = BackpackCreate(**item_data).model_dump()
        item = Backpack(**validated_data)
    elif item_type == "pistol":
        validated_data = PistolCreate(**item_data).model_dump()
        item = Pistol(**validated_data)
    else:
        validated_data = ItemBase(**item_data).model_dump()
        item = Item(**validated_data)

    async with session() as async_session:
        async_session.add(item)
        await async_session.commit()
        await async_session.refresh(item)
        return item


# === Получить предмет по ID ===
async def get_item_by_id(item_id: int):
    session_factory = AsyncSessionLocal
    async with session_factory() as async_session:  # ← создаём сессию
        result = await async_session.execute(
            select(Item)
            .filter(Item.id == item_id)
        )
        return result.scalar_one_or_none()
