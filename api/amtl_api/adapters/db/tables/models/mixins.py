from datetime import datetime

from sqlalchemy import BigInteger, Boolean, DateTime, Sequence, String, func, text
from sqlalchemy.orm import Mapped, declared_attr, mapped_column


class IdMixin:

    __tablename__: str = "IdMixin default"

    @declared_attr
    def id(cls):  # noqa
        return mapped_column(
            BigInteger,
            Sequence(f"{cls.__tablename__}_id_seq"),
            autoincrement=True,
            primary_key=True,
            comment=f"Идентификатор {cls.__tablename__}",
            sort_order=-2,
        )


class DtMixin:
    @declared_attr
    def dt(cls):
        return mapped_column(
            DateTime,
            primary_key=True,
            server_default=func.timezone(func.current_setting("TIMEZONE"), func.date_trunc("second", func.now())),
            nullable=False,
            comment="Дата и время",
            index=True,
        )


class UserIdMixin:
    user_id: Mapped[str] = mapped_column(String(180), nullable=False, comment="Идентификатор пользователя.")


class InsertDtMixin:
    """Insert_dt"""
    insert_dt: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.timezone(func.current_setting("TIMEZONE"), text("clock_timestamp()")),
        comment="Дата вставки",
    )


class UpDateMixin(InsertDtMixin):

    update_dt: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.timezone(func.current_setting("TIMEZONE"), text("clock_timestamp()")),
        comment="Дата изменения",
    )


class TreeStructureMixin(IdMixin, UpDateMixin):
    """Структура ИД - парент ИД"""
    parent_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        index=True,
        comment="Идентификатор родителя",
    )

    is_view: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        index=True,
        default=False,
        comment="Признак видимости",
    )
