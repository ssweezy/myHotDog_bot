from utils.database.models import async_session
from utils.database.models import User
from sqlalchemy import select


async def set_user(data):
    tg_id, tg_username, role, category, name, surname,birthday ,phone, reg_date = data
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id,
                             tg_username=tg_username,
                             role=role,
                             category=category,
                             name=name,
                             surname=surname,
                             birthday=birthday,
                             phone=phone,
                             reg_date=reg_date
                             ))
            await session.commit()

