from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# === Базовый класс предмета ===
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    rarity = Column(String, nullable=False)
    power = Column(Integer, default=0)

    # Тип предмета
    type = Column(String)

    __mapper_args__ = {
        "polymorphic_identity": "item",
        "polymorphic_on": type,
        "with_polymorphic": "*"
    }

# === Снаряжение (родитель для оружия/брони/пистолетов) ===
class Equipment(Item):
    __tablename__ = "equipments"

    id = Column(Integer, ForeignKey("items.id"), primary_key=True)
    initiative = Column(Integer, default=0)  # Инициатива

    __mapper_args__ = {
        "polymorphic_identity": "equipment",
    }

# === Оружие (наследует снаряжение) ===
class Weapon(Equipment):
    __tablename__ = "weapons"

    id = Column(Integer, ForeignKey("equipments.id"), primary_key=True)
    damage = Column(Integer, nullable=False)
    crit_chance = Column(Float, default=0.0)    # (0.0 - 1.0)
    crit_damage = Column(Float, default=1.5)

    __mapper_args__ = {
        "polymorphic_identity": "weapon",
    }

# === Броня (на тело) ===
class Armor(Equipment):
    __tablename__ = "armors"

    id = Column(Integer, ForeignKey("equipments.id"), primary_key=True)
    protection = Column(Float, default=0.0)  # Защита (0.0 - 1.0)
    health = Column(Integer, default=0)      # Здоровье

    __mapper_args__ = {
        "polymorphic_identity": "armor",
    }

# === Пистолеты ===
class Pistol(Equipment):
    __tablename__ = "pistols"

    id = Column(Integer, ForeignKey("equipments.id"), primary_key=True)
    damage_bonus = Column(Integer, default=0)  # Бонус урона

    __mapper_args__ = {
        "polymorphic_identity": "pistol",
    }

# === Артефакты ===
class Artifact(Item):
    __tablename__ = "artifacts"

    id = Column(Integer, ForeignKey("items.id"), primary_key=True)
    effect = Column(String)  # Эффект (пока строка)

    __mapper_args__ = {
        "polymorphic_identity": "artifact",
    }

# === Рюкзаки ===
class Backpack(Item):
    __tablename__ = "backpacks"

    id = Column(Integer, ForeignKey("items.id"), primary_key=True)
    slots = Column(Integer, default=1)  # Слоты

    __mapper_args__ = {
        "polymorphic_identity": "backpack",
    }

# === Инвентарь пользователя ===
class Inventory(Base):
    __tablename__ = "inventories"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, nullable=False)  # Telegram ID или ID в БД

    items = relationship("Item", secondary="inventory_items")  # Связь многие-ко-многим

# === Связь инвентарь-предметы ===
class InventoryItem(Base):
    __tablename__ = "inventory_items"

    id = Column(Integer, primary_key=True)
    inventory_id = Column(Integer, ForeignKey("inventories.id"))
    item_id = Column(Integer, ForeignKey("items.id"))
    quantity = Column(Integer, default=1)  # Количество предметов