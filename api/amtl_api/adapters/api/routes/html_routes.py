from logging import getLogger
from time import time
from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from amtl_api.adapters.api.config import api_settings
from amtl_api.app.api.services.site_api import SiteDataService

template_dir = api_settings.JINJA_TEMPLATE
templates = Jinja2Templates(directory=template_dir)

logger = getLogger("fastapi_app")
html_router = APIRouter()


def check_request(request: Request) -> dict:
    logger.info(f"request.session: {request.session}")
    return {
        "request.session": f"{request.session}",
        "request.path_params": f"{request.path_params}"
    }


@html_router.get("/", response_class=HTMLResponse)
async def index_page(
        request: Request,
        commons: Annotated[dict, Depends(check_request)]
) -> HTMLResponse:
    item_id: int = 1
    return templates.TemplateResponse(
        name="item.jinja", context={"request": request, "item_id": item_id}
    )


@html_router.get("/doc/{item_id}", response_class=HTMLResponse)
async def index_items(
        request: Request,
        item_id: int,
        commons: Annotated[dict, Depends(check_request)],
        service: Annotated[SiteDataService, Depends(SiteDataService)]
) -> HTMLResponse:
    logger.debug(f"Request: {request}")
    logger.debug(f"Commons: {commons}")
    data = await service.get_data()
    logger.debug(f"Service: {data}")
    return templates.TemplateResponse(
        request=request, name="item.jinja", context={"item_id": item_id}, media_type="text/html"
    )


@html_router.get("{path:path}", response_class=HTMLResponse)
async def url(
    request: Request,
    path: str
) -> HTMLResponse:
    t0 = time()
    logger.debug(f"Request: {request}")
    document: str = templates.TemplateResponse(
        request=request, name="base.jinja", context={"item_id": 0, "path": path}
    )
    logger.debug(f"Request path: [{path}] timing: {(time() - t0) * 1000:.4f} ms")
    return document
