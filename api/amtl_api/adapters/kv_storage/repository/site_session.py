from amtl_api.adapters.kv_storage.kv_pool import RedisStorage

# from amtl_api.adapters.kv_storage.settings import Settings as Redis_Settings
from amtl_api.app.api.entities.base import SessionDTO
from amtl_api.app.api.interfaces.session_interfase import SiteSession


class Session(SiteSession):

    redis_client: RedisStorage

    async def get_session(self, session_id: str,) -> SessionDTO | None:
        session: dict | None = await self.redis_client.get(session_id)
        return SessionDTO(**session) if isinstance(session, dict) else None

    async def set_session(self, session: SessionDTO,) -> bool:
        return await self.redis_client.set(session.session_id, session)
