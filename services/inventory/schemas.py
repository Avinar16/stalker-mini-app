from pydantic import BaseModel
from typing import List, Optional

# === Базовая схема предмета ===
class ItemBase(BaseModel):
    name: str
    rarity: str
    power: int = 0

class ItemCreate(ItemBase):
    type: str  # "weapon", "armor", "artifact", "backpack", "pistol"
    # Поля для каждого типа будут разными

class ItemResponse(ItemBase):
    id: int
    type: str

    class Config:
        from_attributes = True

# === Схемы для каждого типа ===
class WeaponCreate(ItemBase):
    type: str = "weapon"
    damage: int
    crit_chance: float
    crit_damage: float

class ArmorCreate(ItemBase):
    type: str = "armor"
    protection: float
    health: int

class ArtifactCreate(ItemBase):
    type: str = "artifact"
    effect: str

class BackpackCreate(ItemBase):
    type: str = "backpack"
    slots: int

class PistolCreate(ItemBase):
    type: str = "pistol"
    damage_bonus: int