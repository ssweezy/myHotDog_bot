from utils.database.models import async_session
from utils.database.models import User
from sqlalchemy import select


# добавление сотрудника в бд
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


# получение кол-ва баллов сотрудника
async def get_points(tg_id):
    async with async_session() as session:
        points = await session.scalar(select(User.points).where(User.tg_id == tg_id))
        return points


# проверка зареган юзер или нет
async def user_exists(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        return True if user else False  # однострочное условие возвращает True/False,


# получение всех сотрудников
async def get_employees():
    async with async_session() as session:
        return await session.scalars(select(User).where(User.category == "emp"))