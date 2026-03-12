from typing import Literal, get_args

from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from .mixins import IdMixin, InsertDtMixin
from .schemas import CommonBase


DATATYPES = Literal[
    "float", "string", "integer", "boolean", "datetype", "decimal", "json", "xml", "toml", "yaml", "csv"
]


class SiteConfig(CommonBase, IdMixin, InsertDtMixin):
    __tablename__ = "site_config"
    __table_args__ = {
        "info": {"title": "Параметры конфигурации сайта"}, "comment": "Параметры конфигурации сайта.",
    }

    key: Mapped[str] = mapped_column(String(30), nullable=False)
    name: Mapped[str | None] = mapped_column(String(255))
    value:  Mapped[str] = mapped_column(String, nullable=False)
    value_type: Mapped[DATATYPES] = mapped_column(
        Enum(
            *get_args(DATATYPES), name="value_data_type", create_constraint=True, validate_strings=True,
        ),
        nullable=False
    )
