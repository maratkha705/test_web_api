from abc import ABC, abstractmethod


class SiteDataInterface(ABC):

    @abstractmethod
    async def get_data(self):  ...

    @abstractmethod
    async def get_document_by_id(self, doc_id: int):  ...

    @abstractmethod
    async def add_document(self, components: dict[int: str],):  ...

    @abstractmethod
    async def update_document(
        self,
        doc_id: int,
        components: dict[int: str],
    ):  ...
