from asyncpg import create_pool
import asyncio
from src.config import db as config, error_codes


class DBAccess(object):
    def __init__(self, engine):
        self.engine = engine

    @classmethod
    async def create(cls, db_url, **kwargs):
        engine = await create_pool(db_url, **kwargs)
        return cls(engine)

    def close(self):
        self.engine.close()


event_loop = asyncio.get_event_loop()
db_url = config.URL_TEMPLATE.format(
    db_host=config.HOST,
    db_name=config.NAME,
    db_user=config.USER,
    db_password=config.PASSWORD
)
dbaccess = db_url is not None and config.POOL_MIN_SIZE is not None and \
           config.POOL_MAX_SIZE is not None and config.TIMEOUT is not None and \
           event_loop.run_until_complete(DBAccess.create(db_url,
                                                         min_size=config.POOL_MIN_SIZE,
                                                         max_size=config.POOL_MAX_SIZE,
                                                         timeout=config.TIMEOUT))


async def fetch(query):
    try:
        async with dbaccess.engine.acquire() as conn:
            return await conn.fetch(query)
    except Exception as e:
        e.code_string = error_codes.DB_ERROR
        raise


async def execute(query):
    try:
        async with dbaccess.engine.acquire() as conn:
            await conn.execute(query)
    except Exception as e:
        e.code_string = error_codes.DB_ERROR
        raise


async def executeval(query, values):
    try:
        async with dbaccess.engine.acquire() as conn:
            await conn.execute(query, *values)
    except Exception as e:
        e.code_string = error_codes.DB_ERROR
        raise
