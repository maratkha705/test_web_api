from sqlalchemy import func
from sqlalchemy.sql.sqltypes import TypeEngine
from sqlalchemy.types import UserDefinedType


class Geography(UserDefinedType):
    # Type Geography deprecated
    _col_spec: str = "geography"

    def get_col_spec(self, **kw):
        return self._col_spec

    def bind_processor(self, dialect):
        def process(value):
            point_string = value
            return func.STGeomFromText(point_string, 4326, type_=self)

        return process

    def bind_expression(self, bindvalue):
        return func.ST_GeomFromText(bindvalue, 4326, type_=self)

    def column_expression(self, col):
        return func.ST_AsText(col, type_=self)


class GEOGRAPHY(TypeEngine):
    # Actual
    __visit_name__ = "geography"

    def __init__(self, point_type: str = 'PointZ', srid: int = 4326):
        # e.g. 'PointZ'
        self.point_type = point_type
        # e.g. '4326'
        self.srid = srid


class GeographyPoint(UserDefinedType):
    #  Geography('POINT', srid='4326')
    _col_spec = 'GEOGRAPHY'

    def get_col_spec(self):
        return self._col_spec

    def bind_expression(self, bindvalue):
        return func.ST_GeomFromText(bindvalue, type_=self)

    def column_expression(self, col):
        return func.ST_AsText(col, type_=self)