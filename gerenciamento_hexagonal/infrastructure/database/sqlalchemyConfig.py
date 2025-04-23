from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from gerenciamento_hexagonal.infrastructure.settings import Settings


engine = create_async_engine(Settings().DATABASE_URL)

AsyncSessionLocal = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


@asynccontextmanager
async def get_session():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()



'''
--- SQLITE ---
engine = create_async_engine(Settings().DATABASE_URL, connect_args={'check_same_thread': False})


@event.listens_for(engine.sync_engine, 'connect')
def enable_foreign_keys(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute('PRAGMA foreign_keys=ON')
    cursor.close()
'''
