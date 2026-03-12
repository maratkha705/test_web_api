from pathlib import Path

from pydantic_settings import BaseSettings  # , SettingsConfigDict


class Settings(BaseSettings):
    # model_config = SettingsConfigDict(env_file=".env", extra="allow")

    API_NAME: str = "AMTL web site"
    API_VER: str = "0.1.1"
    IS_DEBUG: bool = True
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8090
    API_WORKERS: int = 2

    UVICORN_LOG_LEVEL: str = "error"

    STATIC_DIR: Path | str = Path("/data/_AMTL_/web_service/ui")
    TEMPLATE_DIR: Path | str = Path(__file__).parent / "templates"
    TEMPLATE_40X: Path | str = TEMPLATE_DIR / "40x.tpl"

    SESSION_COOKIE_MAX_AGE: int = 86400 * 365
    SESSION_COOKIE_NAME: str = "sess_id"
    SESSION_SECRET_KEY: str = "Se-sAsDsFsB-2drfW_qw3_ew2_qe1_Q"

    @property
    def JINJA_TEMPLATE(self) -> Path:
        return self.STATIC_DIR / "jinja_tpl"


class LogConfig(BaseSettings):
    LOGGER_NAME: str = "amtl_log"
    LOGGING_LEVEL: str = "DEBUG"

    # file handler vars
    LOGGING_MAX_LOG_SIZE: int = 1024*1024*50
    LOGGING_BACKUP_COUNT: int = 10

    FORMAT: str = (
        "%(asctime)s [%(msecs)03d] | %(levelname)s | %(name)s  | %(message)s | %(filename)s.%(funcName)s:%(lineno)d"
    )
    DATE_FORMAT: str = "%Y-%m-%dT%H:%M:%S%Z"
    LOG_PATH: Path | str = Path(__file__).parent.parent.parent.parent / "log/app.log"
    LOG_PATH_ERROR: Path | str = Path(__file__).parent.parent.parent.parent / "log/app_error.log"
