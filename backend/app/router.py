from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.repository import RectangleRepository, IntersectionRepository
from app.schemas import SRectangleAdd, SRectangle, SRectangleId


router_health = APIRouter(prefix='/health')


@router_health.get('/', tags=['Проверка'])
def health_check() -> dict:
    '''Проверка состояния API.'''
    return {'status': 'ok'}


router_rectangle = APIRouter(
    prefix='/rectangles',
    tags=['Прямоугольники'],
)


@router_rectangle.post('/')
async def add_rectangle(rectangle: SRectangleAdd) -> SRectangleId:
    rectangle_id = await RectangleRepository.add_one(rectangle)
    return SRectangleId(rectangle_id=rectangle_id)


@router_rectangle.get('/')
async def get_rectangles() -> list[SRectangle]:
    rectangles = await RectangleRepository.get_all()
    return rectangles


@router_rectangle.delete('/')
async def delete_rectangle(rectangle_id: Annotated[int, Query()]) -> dict:
    await RectangleRepository.delete_one(rectangle_id)
    return {'ok': True, 'message': f'Rectangle {rectangle_id} deleted'}



@router_rectangle.post('/intersect')
async def intersect_rectangles(
    rectangle1_id: Annotated[int, Query()],
    rectangle2_id: Annotated[int, Query()],
) -> dict:
    area = await IntersectionRepository.intersect_and_save(rectangle1_id, rectangle2_id)
    return {'intersection_area': area}