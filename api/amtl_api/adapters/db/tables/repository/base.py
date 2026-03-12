import logging

from sqlalchemy import NullPool, Select, select
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession

from amtl_api.adapters.db.pg_db import PgDB
from amtl_api.adapters.db.settings import Settings
from amtl_api.adapters.shared.tools import component

logger = logging.getLogger('pg_db_logger')

settings: Settings = Settings()
logger.debug(f"Settings: {settings.AMTL_DB_NAME}")


@component(init=False)
class BaseRepository:
    db:PgDB = PgDB(url=settings.db_uri)
    db_name: str = settings.AMTL_DB_NAME
