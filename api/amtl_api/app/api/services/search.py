from amtl_api.adapters.api.config import logger
from amtl_api.adapters.api.exceptions import ApiBaseException
from amtl_api.adapters.db.tables.repository.site_config import SiteConfRepo

from ..entities.base import TestSchema
from ..interfaces.site_api import SiteDataInterface


class SiteSearchService(SiteDataInterface):
    repo: SiteConfRepo = SiteConfRepo()

    async def get_data(self):

        try:
            site_config = await self.repo.get_config()
        except Exception as ex:
            logger.debug(f"SiteConfig error: {ex}")
            site_config = {
                "ex": f"Fail: {ex}"
            }
        return TestSchema(
            title="1", notes=[1, 2, 3, 4], data=site_config, description="",
        )

    async def get_document_by_id(self, doc_id: int):
        raise ApiBaseException(message="Method not implemented", status_code=404)

    async def add_document(self, components: dict[int: str],):
        raise ApiBaseException(message="Method not implemented", status_code=404)

    async def write_document(self, doc_id: int, components: dict[int: str],):
        raise ApiBaseException(message="Method not implemented", status_code=404)

