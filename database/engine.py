from database.models import Base
from database.models.settings import Settings

from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker  
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession


class Database:

    def __init__(self, database_url: str):

        self.engine = create_async_engine(
            database_url, future=True, pool_pre_ping=True
        )
        self.sessionmaker = sessionmaker(
            self.engine, expire_on_commit=False, class_=AsyncSession
        )

    async def create_tables(self):

        async with self.engine.begin() as conn:
                
            await conn.run_sync(Base.metadata.create_all)

        async with self.sessionmaker() as session: 

            save_exists = await session.execute(
                select(Settings)
            )

            if not save_exists.all():

                session.add(Settings())
                await session.commit()


    @classmethod
    async def init(cls, database_url: str) -> "Database":

        instance = cls(database_url)
        await instance.create_tables()

        return instance


async def create_sessionmaker(database_url: str) -> sessionmaker:

    database = await Database.init(database_url)

    return database.sessionmaker
