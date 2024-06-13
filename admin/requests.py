from utils.database.models import async_session
from utils.database.models import User
from sqlalchemy import select


async def get_employees():
    async with async_session() as session:
        return await session.scalars(select(User))