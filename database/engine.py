import os
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
import config_data
from database.models import Base

# from .env file:
# DB_LITE=sqlite+aiosqlite:///my_base.db
# DB_URL=postgresql+asyncpg://login:password@localhost:5432/db_name
config: config_data.Config = config_data.load_config()  # load_config('.env')
engine = create_async_engine(config.db.db_lite, echo=True)
# engine = create_async_engine(os.getenv('DB_URL'), echo=True)

session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
