from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки соединения с базой данных"""
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    # Data base connect parameters
    AMTL_DB_HOST: str = "localhost"
    AMTL_DB_NAME: str = ""
    AMTL_DB_USER: str = ""
    AMTL_DB_PASS: str = ""
    AMTL_DB_PORT: int = 5432

    AMTL_DB_ECHO: bool = True
    AMTL_DB_PRE_PING: bool = True
    AMTL_DB_POOL_RECYCLE: int = 3600
    AMTL_DB_CONNECTION_NAME: str = "Amtl_web_api"
    AMTL_DB_LOGGING: bool = False
    AMTL_DB_DEBUG: bool = False
    AMTL_DB_TYPE: str = "pg"
    AMTL_DB_COMMENT: str = ""

    @property
    def db_uri(self) -> str:
        return f"postgresql+asyncpg://{self.AMTL_DB_USER}:{self.AMTL_DB_PASS}"\
               f"@{self.AMTL_DB_HOST}:{self.AMTL_DB_PORT}/{self.AMTL_DB_NAME}"

    # alembic
    ALEMBIC_LOG_LOCATION: str = "amtl_api/adapters/db/alembic"
    ALEMBIC_SCRIPT_LOCATION: str = "amtl_api.adapters.db:alembic"
    ALEMBIC_VERSION_LOCATIONS: str = "amtl_api.adapters.db.alembic:migrations"
    ALEMBIC_MIGRATION_FILENAME_TEMPLATE: str = (
        "%%(year)d_"
        "%%(month).2d_"
        "%%(day).2d_"
        "%%(hour).2d_"
        "%%(minute).2d_"
        "%%(second).2d_"
        "%%(slug)s"
    )


def get_settings() -> Settings:
    return Settings()
