from asyncio import run as asyncio_run

from alembic import context
import logging
from sqlalchemy import MetaData, engine_from_config, pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncEngine

from amtl_api.adapters.db.tables.models.schemas import CommonBase, DataBase
from amtl_api.adapters.db.settings import Settings

logger = logging.getLogger('pg_db_logger')

settings: Settings = Settings()
logger.debug(f"Settings: {settings.AMTL_DB_NAME}")


config = context.config


def combine_metadata(*args):
    m = MetaData()
    for metadata in args:
        for t in metadata.tables.values():
            logger.debug(f"Meta: {t}")
            t.tometadata(m)
    return m


logger.debug(f"CommonBase.metadata: {CommonBase.metadata}")
logger.debug(f"DataBase.metadata: {DataBase.metadata}")
target_metadata = combine_metadata(CommonBase.metadata, DataBase.metadata)


def run_migrations_online():
    connectable = context.config.attributes.get("connection", None)
    if connectable is None:
        connectable = AsyncEngine(
            engine_from_config(
                context.config.get_section(context.config.config_ini_section),
                prefix="sqlalchemy.",
                poolclass=pool.NullPool,
                future=True
            )
        )

    if isinstance(connectable, AsyncEngine):
        asyncio_run(run_async_migrations(connectable))
    else:
        do_run_migrations(connectable)


def include_name(name, type_, parent_names):
    if type_ == "table":
        return (
            parent_names["schema_qualified_table_name"]
            in target_metadata.tables
        )
    else:
        return True


async def run_async_migrations(connectable):
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
        include_name=include_name,
        include_schemas=True,
    )

    with context.begin_transaction():
        context.run_migrations()


run_migrations_online()
