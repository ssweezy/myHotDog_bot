from utils.database.models import async_session
from utils.database.models import User
from sqlalchemy import select, update, delete


# добавление сотрудника в бд
async def set_user(data):
    tg_id, tg_username, role, category, name, surname, birthday, phone, reg_date, msg_id, chat_id = data
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
                             reg_date=reg_date,
                             msg_id=msg_id,
                             chat_id=chat_id
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


# получение всю информацию о пользователе с помощью его ID
async def get_user_info(tg_id):
    async with async_session() as session:
        return await session.scalar(select(User).where(User.tg_id == tg_id))


# получение всех сотрудников
async def get_employees():
    async with async_session() as session:
        return await session.scalars(select(User).where(User.category == "emp"))


# меняет количество очков пользователя используя его айди
async def update_user_points(tg_id, new_value: int):
    async with async_session() as session:
        await session.execute(update(User).where(User.tg_id == tg_id).values(points=new_value))
        await session.commit()


async def update_msg_id(tg_id, new_value):
    async with async_session() as session:
        await session.execute(update(User).where(User.tg_id == tg_id).values(msg_id=new_value))
        await session.commit()