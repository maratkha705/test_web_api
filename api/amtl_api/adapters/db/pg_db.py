# TODO докстринги, логирование в адаптер
from collections.abc import AsyncIterator
from typing import Any, AsyncGenerator
from contextlib import asynccontextmanager
from logging import DEBUG, basicConfig, getLogger

# from asyncpg.exceptions import PostgresSyntaxError
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

basicConfig(
    format='%(asctime)s ms=%(msecs)03d | %(levelname)s | %(message)s [%(filename)s::%(lineno)d]', level=DEBUG
)
logger = getLogger("pgdb")


class PgException(Exception):
    def __init__(self, message: str, errors: str | list | dict | None = None):
        super().__init__(message)
        self.errors = errors


class PgDB:
    session_id = 0
    connect_id = 0

    def __init__(
            self, url: str, pool_pre_ping: bool = False, pool_recycle: int = 7200, echo: bool = False,
            connection_name: str = "amtl"
    ):
        self._url = url
        self._engine: AsyncEngine = create_async_engine(
            url, echo=echo, pool_recycle=pool_recycle, pool_pre_ping=pool_pre_ping,
            connect_args={"server_settings": {"application_name": connection_name}},
        )
        self._sessionmaker = async_sessionmaker(autocommit=False, bind=self._engine)

    @asynccontextmanager
    async def connect(self) -> AsyncGenerator[AsyncConnection, Any]:
        connect: AsyncConnection = await self._engine.connect()
        db_url_name = self._url.split('@')[-1]
        try:
            self.connect_id += 1
            logger.info(f"Try connect to {db_url_name} / {self.connect_id}")
            yield connect
        except Exception as exc:
            await connect.rollback()
            await connect.close()
            logger.error(f"Fail connect to {db_url_name} / {self.connect_id}: {exc.args[0][:256]}")
        finally:
            await connect.close()
            logger.debug(f"Connect <{db_url_name}/{self.connect_id}> closed")

    def get_session(self) -> AsyncSession:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        self.session_id += 1
        return session

    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        session: AsyncSession = self.get_session()
        try:
            logger.info(f"Try get new session {self.session_id}")
            yield session
        except Exception as exc:
            await session.rollback()
            await session.close()
            logger.error(f"fail session {self.session_id} / {type(exc)} / {exc.args[0]}")
            # raise PgException(message=f"Fail session {self.session_id}: {exc.args[0]}")
        finally:
            logger.info(f"session close {self.session_id}")
            await session.close()
