from abc import ABC, abstractmethod
from amtl_api.app.api.entities.base import SessionDTO


class SiteSession(ABC):

    @abstractmethod
    async def get_session(self, session_id: str,) -> SessionDTO | None: ...

    @abstractmethod
    async def set_session(self, session: SessionDTO,) -> bool:  ...
