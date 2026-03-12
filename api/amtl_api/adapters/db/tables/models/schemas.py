from sqlalchemy import MetaData
from sqlalchemy.orm import as_declarative


convention = {
  "ix": "ix_%(column_0_label)s",
  "uq": "uq_%(table_name)s_%(column_0_name)s",
  "ck": "ck_%(table_name)s_%(constraint_name)s",
  "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
  "pk": "pk_%(table_name)s"
}


@as_declarative(metadata=MetaData(schema="common", naming_convention=convention))
class CommonBase:
    ...


@as_declarative(metadata=MetaData(schema="data", naming_convention=convention))
class DataBase:
    ...


@as_declarative(metadata=MetaData(schema="log", naming_convention=convention))
class LogBase:
    ...


@as_declarative(metadata=MetaData(schema="api_info", naming_convention=convention))
class ApiInfoBase:
    ...


@as_declarative(metadata=MetaData(schema="api_logs", naming_convention=convention))
class ApiInfoBase:
    ...

