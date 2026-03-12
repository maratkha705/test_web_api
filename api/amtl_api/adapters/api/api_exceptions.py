from string import Template

from fastapi import HTTPException, Request, Response
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError, WebSocketRequestValidationError
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.websockets import WebSocket
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY, WS_1008_POLICY_VIOLATION

from amtl_api.adapters.api.config import api_settings, logger

from .lifespan import AppJSONResponse

with open(api_settings.TEMPLATE_40X) as f:
    HTML_TEMPLATE: Template = Template(f.read())


def _response(url: str, message: str | list | dict, status_code: int,  **args):
    if url.startswith('/api/xml'):
        return Response(content=message, status_code=status_code, media_type="application/xml")
    if url.startswith('/api/plain'):
        return PlainTextResponse(content=f"failure\n{message}", status_code=status_code)
    if url.startswith('/api'):
        return AppJSONResponse(
            content={"status": "failure",  "detail": message}, status_code=status_code
        )
    else:
        content = HTML_TEMPLATE.substitute(
            {
                "detail": message,
                "status_code": status_code,
                "url": url
            }
        )
        return HTMLResponse(content=content, status_code=status_code)


def api_exception_handler(request: Request, exc: HTTPException) -> Response:
    getattr(exc, "headers", None)
    logger.error(f"{request.url.path}: {exc}")
    return _response(url=request.url.path, message=exc.detail, status_code=exc.status_code)


def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> AppJSONResponse:
    logger.error(f"{request.url.path} : {exc}")
    return AppJSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": jsonable_encoder(exc.errors())
        },
    )


async def websocket_request_validation_exception_handler(
    websocket: WebSocket, exc: WebSocketRequestValidationError
) -> None:
    await websocket.close(
        code=WS_1008_POLICY_VIOLATION, reason=jsonable_encoder(exc.errors())
    )
