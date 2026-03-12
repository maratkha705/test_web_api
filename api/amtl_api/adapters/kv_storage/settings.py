from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    AMT_REDIS_HOST: str
    AMT_REDIS_PORT: int
    AMT_REDIS_DB: int
    AMT_REDIS_USER: str
    AMT_REDIS_PASSWORD: str

    def get_url(self) -> str:
        return (
            f"redis://{self.AMT_REDIS_USER}:{self.AMT_REDIS_PASSWORD}"  # noqa
            f"@{self.AMT_REDIS_HOST}:{self.AMT_REDIS_PORT}/{self.AMT_REDIS_DB}")  # noqa
