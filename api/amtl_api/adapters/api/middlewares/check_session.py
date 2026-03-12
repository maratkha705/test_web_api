from collections.abc import Callable
from datetime import datetime
from inspect import iscoroutinefunction
from typing import Any
from uuid import uuid4

from fastapi import FastAPI, Request, Response

from amtl_api.adapters.api.config import logger
from amtl_api.adapters.kv_storage.repository.site_session import Session
from amtl_api.app.api.entities.base import SessionDTO
from amtl_api.app.api.interfaces.session_interfase import SiteSession

from amtl_api.adapters.api.api_tools import check_url
from amtl_api.adapters.api.check_user import is_bot
from amtl_api.adapters.api.exceptions import ApiBaseException
from amtl_api.adapters.api.models import DocumentUrl


def session_middleware(app: FastAPI, api_settings) -> None:

    def _check_url(request: Request) -> DocumentUrl:
        hostname = request.url.hostname
        url, parent_url = check_url(request.url.path)
        logger.debug(f"Host: {hostname}, url: {url}, parent: {parent_url}")
        if url != request.url.path:
            raise ApiBaseException(message=f"Wrong url: {request.url.path}={url}", pid=request.app.state.pid)

        user_agent = request.headers.get("user-agent")
        user_is_bot = is_bot(user_agent=user_agent)

        query_params = request.query_params
        host_sections = hostname.split(".")
        if len(host_sections) > 1:
            zone = host_sections.pop(-1)
            hostname = host_sections.pop(-1)
            subdomain = ".".join(host_sections) if len(host_sections) > 0 else "www"
        else:
            zone = "loc"
            subdomain = "www"

        return DocumentUrl(
            subdomain=subdomain,
            domain=hostname,
            path=url,
            zone=zone,
            query_params=query_params,
            is_bot=user_is_bot
        )

    async def set_session(request: Request, response: Response):
        session_id = request.cookies.get(api_settings.SESSION_COOKIE_NAME, None)
        session_repo: SiteSession = Session()
        if session_id is None:
            max_age = api_settings.SESSION_COOKIE_MAX_AGE
            session_id = str(uuid4())
            logger.info(f"Start session: Id={session_id} {request.url}")
            response.set_cookie(
                key=api_settings.SESSION_COOKIE_NAME, value=session_id, httponly=True,
                max_age=max_age, expires=max_age, samesite="strict"
            )
            session = None
        else:
            session = await session_repo.get_session(session_id)

        if session is None:
            session = SessionDTO(
                session_id=session_id,
                session_at=datetime.now(),
                session_up=datetime.now(),
                session_counter=0
            )
        session.session_counter += 1
        add_session = await session_repo.set_session(session)
        logger.debug(f"Session done: {session.session_id}, {add_session}")
        _session = await session_repo.get_session(session_id)
        logger.debug(f"Session check: {session.session_id}, {_session}")

    @app.middleware("http")
    async def check_session(request: Request, call_next: Callable[[Request, Any]]):
        url_data = _check_url(request)
        request.state.url_data = url_data
        try:
            if not iscoroutinefunction(call_next):
                response: Response = call_next(request)
            else:
                response: Response = await call_next(request)
        except ApiBaseException:
            raise

        if not url_data.is_bot:
            await set_session(request, response)

        logger.info(f"End: {request.url}, status: {response.status_code}")
        return response
