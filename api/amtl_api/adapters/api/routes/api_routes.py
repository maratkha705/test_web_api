from datetime import datetime
# from decimal import Decimal
from logging import getLogger
from pathlib import Path, PosixPath

import aiofiles
from fastapi import APIRouter, Depends, Form, Request, UploadFile

from amtl_api.adapters.api.lifespan import AppJSONResponse
from amtl_api.app.api.entities.base import TestSchema
from amtl_api.app.api.services.site_api import SiteDataService

logger = getLogger("fastapi_app")

api_router = APIRouter()


@api_router.get("/", response_model=TestSchema, response_class=AppJSONResponse)
async def index_page(
    service: SiteDataService = Depends(SiteDataService),
) -> TestSchema:
    return await service.get_data()


@api_router.get("/info", response_model=TestSchema, response_class=AppJSONResponse)
async def info_page(
    service: SiteDataService = Depends(SiteDataService),
) -> TestSchema:
    return await service.get_data()


async def upload_file_by_(file_path: str | Path, file):
    chunk_size: int = 1024 * 1024
    mode = "ab"
    async with aiofiles.open(file_path, mode) as f:  # type: ignore
        while _chunk := await file.read(chunk_size):
            await f.write(_chunk)


@api_router.post("/upload", response_class=AppJSONResponse)
async def upload(file: UploadFile, chunk: int = Form()) -> dict:
    logger.info(f"Chunk: {chunk}")
    file_path = Path("/data/INTEGRAL/db-csv/test.xxx")  # type: ignore
    await upload_file_by_(file_path, file)

    logger.info(f"Saved: {chunk}")
    return {"message": chunk}


@api_router.get("{path:path}", response_class=AppJSONResponse)
async def url(
    request: Request,
    path: str
) -> dict:
    return {
        "path": path,
        "now": datetime.now().strftime("%Y-%m-%dT%H-%M-%S"),
        "url": request.url,
        "ycx": 1,
        "ppu": dir(request.state)
    }



