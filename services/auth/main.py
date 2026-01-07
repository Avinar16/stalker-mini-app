from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from db import AsyncSession
from models import *
from settings import settings
app = FastAPI()

# WIP
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.allowed_origins],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/greet")
async def verify_telegram_auth(session: AsyncSession):
    async with session.begin() as db:
        result = await db.execute(select(User))
        return result.scalars().all()

@app.post("/user")
async def verify_telegram_auth(session: AsyncSession):
    async with session.begin() as db:
        result = await db.add()
        return result.scalars().all()