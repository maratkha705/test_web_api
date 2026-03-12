from datetime import datetime

from dataclasses import dataclass
from decimal import Decimal
from pydantic import BaseModel, Field


class DotDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class TestSchema(BaseModel):
    title: str = Field(..., min_length=1, max_length=64)
    notes: list[int] = Field(min_length=0)
    data: dict = Field(default_factory=dict)
    description: str = Field(..., min_length=1, max_length=64)


@dataclass(slots=True)
class SessionDTO(DotDict):
    session_id: str
    session_at: datetime
    session_up: datetime
    session_role: str = ""
    session_counter: int = 0    

    def __post_init__(self):
        if isinstance(self.session_at, str):
            self.session_at = datetime.strptime(self.session_at, "%Y-%m-%d %H:%M:%S.%f")
        if isinstance(self.session_up, str):
            self.session_up = datetime.strptime(self.session_up, "%Y-%m-%d %H:%M:%S.%f")


@dataclass(slots=True)
class IdMixin:
    id: int | None = None


class UpdateDateMixin(IdMixin):
    inserted_at: datetime
    updated_at: datetime
    review_at: datetime


class Item(UpdateDateMixin):
    name: str
    count: int
    price: Decimal


class SiteMap(UpdateDateMixin):
    id: int
    subdomain: str
    path: str
    parent: str
    name: str
    title: str
    description: str
    meta: dict
    services: list[str]
    doc_type: int
    sort_order: int
    is_view: bool | None = None
    is_hit: bool | None = None
    is_top: bool | None = None
