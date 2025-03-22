from pydantic import BaseModel, ConfigDict


class SRectangleAdd(BaseModel):
    x1: float
    y1: float
    x2: float
    y2: float


class SRectangle(SRectangleAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class SRectangleIntersectionAdd(BaseModel):
    rectangle1_id: int
    rectangle2_id: int
    intersection_area: float


class SRectangleIntersection(SRectangleIntersectionAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class SRectangleId(BaseModel):
    ok: bool = True
    rectangle_id: int


class SRectangleIntersectionId(BaseModel):
    ok: bool = True
    intersection_id: int
