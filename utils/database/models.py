from sqlalchemy import BigInteger, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

#создание файла
engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')

#создание подключения
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    tg_username: Mapped[str] = mapped_column(String(30))
    role: Mapped[str] = mapped_column(String(20))
    category: Mapped[str] = mapped_column(String(20))
    name: Mapped[str] = mapped_column(String(30))
    surname: Mapped[str] = mapped_column(String(30))
    birthday: Mapped[str] = mapped_column(String(30))
    phone: Mapped[str] = mapped_column(String(30))
    reg_date: Mapped[str] = mapped_column(String(40))
    points: Mapped[int] = mapped_column(default=0)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)