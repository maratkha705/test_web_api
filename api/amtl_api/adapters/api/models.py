from typing import Any

from pydantic import BaseModel, Field


class DocumentUrl(BaseModel):
    subdomain: str = Field(..., min_length=1, max_length=255)
    domain: str = Field(..., min_length=1, max_length=255)
    zone: str = Field(..., min_length=1, max_length=32)
    path: str = Field(..., min_length=1, max_length=1024)
    query_params: dict[str, Any] = Field(default_factory=dict)
    is_bot: bool = False
    is_view: bool = False


class TestSchema(BaseModel):
    title: str = Field(..., min_length=1, max_length=64)
    description: str = Field(..., min_length=1, max_length=64)
    notes: list[int] = Field(min_length=0)
    is_bot: bool = False
    is_view: bool = False
