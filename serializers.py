from typing import Optional, List

from geoalchemy2.shape import from_shape, to_shape
from shapely.geometry import Polygon

from pydantic import BaseModel, root_validator
from sqlalchemy import func

from features import make_polygon_from_list


def create_polygon_for_db(coordinates: List[List[float]]) -> Polygon:
    polygon = from_shape(
        Polygon(coordinates)
    )
    return polygon


class ZoneBase(BaseModel):
    currier: Optional[int]


class ZoneToAssign(BaseModel):
    zone_id: int
    currier: int


class ZoneReturn(ZoneBase):
    zone_coordinates:  List[List[float]]
    id: int

    class Config:
        orm_mode = True

    @root_validator(pre=True)
    def convert_coords_to_list(cls, values):
        values = dict(values)
        obj_coords = values.get("zone_coordinates")
        values["zone_coordinates"] = [coord for coord in to_shape(obj_coords).boundary.coords]
        return values


class ZoneCreate(ZoneBase):
    zone_coordinates: List[List[float]]

    @root_validator
    def convert_to_str(cls, values):
        values = dict(values)
        obj_coords = values.get("zone_coordinates")
        values["zone_coordinates"] = make_polygon_from_list(obj_coords)
        return values


class Point(BaseModel):
    coords: List[float]


def make_point_obj_from_point(point: Point):
    point_obj = func.ST_GEOMFROMTEXT('POINT({} {})'.format(point.coords[0], point.coords[1]))
    return point_obj
