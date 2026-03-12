from os import getpid

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.sessions import SessionMiddleware

from amtl_api.adapters.api.config import api_settings, logger
from amtl_api.adapters.api.routes.api_routes import api_router
from amtl_api.adapters.api.routes.html_routes import html_router

from amtl_api.adapters.api.middlewares.check_session import session_middleware
from .exceptions import ApiBaseException

PID = getpid()


def exc_handlers(app: FastAPI):
    @app.exception_handler(ApiBaseException)
    def base_api_exc(request: Request, exc: ApiBaseException, status_code: int = 500):
        return JSONResponse(
            status_code=status_code,
            content={
                "url": request.url,
                "message": exc.message,
                "detail": exc.detail,
                "more": exc.more,
            }
        )


def run_app(app: FastAPI) -> FastAPI:
    logger.info("Start loading app")
    app.add_middleware(
        SessionMiddleware,
        secret_key=api_settings.SESSION_SECRET_KEY,
        session_cookie=api_settings.SESSION_COOKIE_NAME
    )

    # exceptions
    logger.debug("Set exc handlers")
    exc_handlers(app)

    # middlewares
    logger.debug("Set middlewares")
    session_middleware(app, api_settings)

    app.include_router(api_router, prefix="/api")
    app.include_router(html_router)
    app.state.pid = PID
    logger.info(f"Running app, PID: {app.state.pid}")
    return app
