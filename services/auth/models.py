from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, func, BigInteger
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    # Информация об аккаунте
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False, index=True)
    username = Column(String, nullable=True)
    role = Column(String, nullable=False, default="user")
    first_name = Column(String, nullable=True)

    # Игровая информация
    level = Column(Integer, default=1)
    experience = Column(Integer, default=0)
    elo_rating = Column(Integer, default=0)

    # Баланс
    ton = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())