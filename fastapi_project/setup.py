import time
from contextlib import asynccontextmanager
from fastapi import Depends
from main import FastAPI
from database.models import engine, Base, session, AsyncSession, Role, User


@asynccontextmanager
async def lifespan(main_app: FastAPI):
    async with engine.begin() as conn:
        time.sleep(5)
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    async_session = session()
    async with async_session:
        await create_datas_in_database(async_session)
    yield
    await engine.dispose()


async def get_session() -> AsyncSession:
    """
    Создание сессии базы данных
    """
    async with session() as async_session:
        yield async_session



async def create_datas_in_database(async_session: AsyncSession = Depends(get_session)):
    user_1 = User(
            name="Aleksey",
            last_name="Zuev",
            email="aleksey@mail.ru",
            phone="+73332221155"
        )
    user_2 = User(
        name="Natalia",
        last_name="Safonova",
        email="natali@mail.ru",
        phone="+74561237896"
        )
    user_3 = User(
        name="Dmitriy",
        last_name="Timoshenko",
        email="d.timon@mail.ru",
        phone="+79991110293"
        )
    role_1 = Role(
        name="Client",
        user_id=1,
        description="A legal entity or individual who uses the services of another individual "
                    "or legal entity and enters into business relations with him."
    )
    role_2 = Role(
        name="Admin",
        user_id=2,
        description="A specialist responsible for maintaining the functionality of the hardware"
                    " and software components of an information system."
    )
    role_3 = Role(
        name="Assistant",
        user_id=3,
        description="A person who is attached to the manager and performs various types of tasks:"
                    " personal or business assignments."
    )


    async_session.add(role_1)
    async_session.add(role_2)
    async_session.add(role_3)
    async_session.add(user_1)
    async_session.add(user_2)
    async_session.add(user_3)
    await async_session.commit()