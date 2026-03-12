from typing import Any, Literal, get_args

from sqlalchemy import Boolean, Enum, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .geo_types import GeographyPoint
from .mixins import IdMixin, TreeStructureMixin, UpDateMixin
from .schemas import DataBase

DOCTYPES = Literal["plain", "article", "category", "items", "service", "report"]
CONTENTYPES = Literal["html", "slider", "gallery", "image", "media", "html_form", "map"]


class GeoObjects(DataBase, IdMixin):
    """ Geo Objects table """
    __tablename__ = "geo_objects"
    __table_args__ = {"comment": "География",}
    name: Mapped[str] = mapped_column(String(255), nullable=False, comment="Наименование объекта")
    coords = mapped_column(GeographyPoint, nullable=False, unique=True, comment="Point(Coords)")


class UserAccount(DataBase, IdMixin, UpDateMixin):
    __tablename__ = "user_account"
    __table_args__ = {
        "info": {"title": "Пользователи"},
        "comment": "Пользователи",
    }

    name: Mapped[str] = mapped_column(String(30), nullable=False)
    full_name: Mapped[str | None] = mapped_column(String)
    phone: Mapped[str | None] = mapped_column(String)
    address: Mapped[list["AddressUser"]] = relationship("AddressUser", back_populates="user")
    user_account: Mapped[list["AddressUser"]] = relationship("AddressUser", back_populates="user")


class AddressUser(DataBase, IdMixin, UpDateMixin):
    __tablename__ = "address_user"
    __table_args__ = {
        "info": {"title": "Пользователи"},
        "comment": "Адрес пользователя",
    }

    email_address: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[int] = mapped_column(
        ForeignKey(UserAccount.id), nullable=False, onupdate="CASCADE", comment="ID пользователя"
    )
    address: Mapped[str] = mapped_column(String, nullable=True)
    phone: Mapped[int] = mapped_column(Integer, nullable=True)

    geo: Mapped[int] = mapped_column(
        ForeignKey(GeoObjects.id), nullable=True, onupdate="CASCADE", comment="Координаты"
    )
    user: Mapped[list["SiteContent"]] = relationship("User", back_populates="user")


class SubDomains(DataBase, IdMixin, UpDateMixin):
    __tablename__ = "subdomains"
    __table_args__ = {
        "info": {"title": "Карта сайта"},
        "comment": "Субдомены сайта, в т.ч. ГЕО",
    }
    name: Mapped[str] = mapped_column(String(127), nullable=False)
    title: Mapped[str] = mapped_column(String(256), nullable=True)
    description: Mapped[str] = mapped_column(String(512), nullable=True)
    geo: Mapped[int] = mapped_column(
        ForeignKey(GeoObjects.id), nullable=True, onupdate="CASCADE", comment="Координаты"
    )
    meta: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=True)
    is_view: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        index=True,
        default=False,
        comment="Признак видимости",
    )
    relevance: Mapped[list[int]] = mapped_column(ARRAY(Integer), nullable=True)


class SiteMap(DataBase, TreeStructureMixin, UpDateMixin):
    __tablename__ = "site_map"
    __table_args__ = {
        "info": {"title": "Карта сайта"},
        "comment": "Карта сайта",
    }
    subdomain_id: Mapped[int] = mapped_column(
        ForeignKey(SubDomains.id), nullable=False, onupdate="CASCADE",
    )
    path: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(127), nullable=False)

    doc_type: Mapped[DOCTYPES] = mapped_column(
        Enum(
            *get_args(DOCTYPES), name="html_document_type", create_constraint=True, validate_strings=True,
        ),
        default="plain",
        nullable=False
    )

    sort_order: Mapped[int] = mapped_column(
        Integer,
        index=True,
        nullable=False,
        default=0,
        comment="Порядок сортировки",
    )

    services: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)
    relevance: Mapped[list[int]] = mapped_column(ARRAY(Integer), nullable=True)
    meta: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=True)


class SiteContent(DataBase, IdMixin, UpDateMixin):
    __tablename__ = "site_content"
    __table_args__ = {
        "comment": "Контент документа",
    }
    document_id: Mapped[int] = mapped_column(
        ForeignKey(SiteMap.id), nullable=False, onupdate="CASCADE", comment="Идентификатор документа"
    )
    content: Mapped[str] = mapped_column(String, nullable=False)
    content_type: Mapped[CONTENTYPES] = mapped_column(
        Enum(
            *get_args(CONTENTYPES), name="content_type", create_constraint=True, validate_strings=True,
        ),
        default="plain",
        nullable=False
    )
    user: Mapped["UserAccount"] = relationship(back_populates="user")
    keywords: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)
    relevance: Mapped[list[int]] = mapped_column(ARRAY(Integer), nullable=True)
    goods: Mapped[list[int]] = mapped_column(ARRAY(Integer), nullable=True)
    articles: Mapped[list[int]] = mapped_column(ARRAY(Integer), nullable=True)
    meta: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=True)
    is_view: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        index=True,
        default=False,
        comment="Признак видимости",
    )
    is_hit: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        index=True,
        default=False,
        comment="Признак хит контент",
    )
    services: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)

