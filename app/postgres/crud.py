from sqlalchemy import select, or_
from pydantic import UUID4

from app.postgres.engine import async_session
from app.postgres.tables import User
from app.schemas import users


async def get_user_by_email_or_username(email_or_username: str) -> users.FullUser:
    db = async_session()
    try:
        user = await db.scalar(select(User).where(or_(User.username == email_or_username,
                                                      User.email == email_or_username)))
        return user
    finally:
        await db.close()


async def get_user_by_id(user_id: UUID4) -> users.FullUser:
    db = async_session()
    try:
        user = await db.scalar(select(User).where(User.id == user_id))
        return user
    finally:
        await db.close()