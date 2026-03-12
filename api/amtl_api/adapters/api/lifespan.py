from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from rapidjson import DM_ISO8601, NM_DECIMAL, UM_CANONICAL, dumps

from amtl_api.adapters.shared import component

from .config import logger


@component
class LifespanLoad:
    app: FastAPI
    name: str = "FastAPI: LifespanLoad"

    def load(self):
        self.app.state.start = 1

        # connect redis etc
        self.app.state.redis = 1
        logger.debug(f"App load: {self.name}, pid={self.app.state.pid} / {self.app.state.redis}")

    def clear(self):
        # close redis etc
        self.app.state.redis = None

        logger.debug(f"App clear: {self.name}, pid={self.app.state.pid}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    _span = LifespanLoad(app=app)
    _span.load()
    yield
    _span.clear()


class AppJSONResponse(JSONResponse):
    def render(self, content: Any) -> bytes:
        return dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            default=str,
            datetime_mode=DM_ISO8601,
            number_mode=NM_DECIMAL,
            uuid_mode=UM_CANONICAL,
        ).encode()
