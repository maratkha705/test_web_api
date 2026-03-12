import logging

from sqlalchemy import Select, select
from sqlalchemy.engine.result import ChunkedIteratorResult

from amtl_api.adapters.db.tables.models.common import SiteConfig

# from sqlalchemy.engine.row import Row
from .base import BaseRepository

logger = logging.getLogger('pg_db_logger')


class SiteConfRepo(BaseRepository):

    async def get_config(self) -> SiteConfig | None:
        query: Select = select(SiteConfig)
        logger.debug("Connect:")
        """
        async with await self.session as session:
            logger.debug("Start query")
            result: ChunkedIteratorResult = await session.execute(query)
        """
        async with self.db.connect as connect:
            logger.debug("Start query")
            result: ChunkedIteratorResult = await connect.execute(query)

            row = result.mappings().one_or_none()
            logger.debug(f"{row=}")
            if row:
                return SiteConfig(**row)
            else:
                return None
