from sqlalchemy import select, and_
from app.database import new_session, RectangleOrm, RectangleIntersectionOrm
from app.schemas import (
    SRectangleAdd,
    SRectangle,
)


class RectangleRepository:
    @classmethod
    async def add_one(cls, data: SRectangleAdd) -> int:
        async with new_session() as session:
            rect_dict = data.model_dump()

            result = await session.execute(
                select(RectangleOrm).where(
                    RectangleOrm.x1 == rect_dict["x1"],
                    RectangleOrm.y1 == rect_dict["y1"],
                    RectangleOrm.x2 == rect_dict["x2"],
                    RectangleOrm.y2 == rect_dict["y2"],
                )
            )
            existing = result.scalar_one_or_none()

            if existing:
                return existing.id

            rectangle = RectangleOrm(**rect_dict)
            session.add(rectangle)
            await session.flush()
            await session.commit()
            return rectangle.id


    @classmethod
    async def get_all(cls) -> list[SRectangle]:
        async with new_session() as session:
            result = await session.execute(select(RectangleOrm))
            rectangle_models = result.scalars().all()
            return [SRectangle.model_validate(model) for model in rectangle_models]

    @classmethod
    async def delete_one(cls, rectangle_id: int) -> None:
        async with new_session() as session:
            await session.execute(
                RectangleOrm.__table__.delete().where(RectangleOrm.id == rectangle_id)
            )
            await session.commit()


class IntersectionRepository:
    
    @staticmethod
    def _calculate_intersection_area(r1: RectangleOrm, r2: RectangleOrm) -> float | None:
        x_left = max(r1.x1, r2.x1)
        y_top = max(r1.y1, r2.y1)
        x_right = min(r1.x2, r2.x2)
        y_bottom = min(r1.y2, r2.y2)

        if x_left < x_right and y_top < y_bottom:
            return (x_right - x_left) * (y_bottom - y_top)
        return None
    
    @classmethod
    async def intersect_and_save(cls, rect1_id: int, rect2_id: int) -> float | None:
        async with new_session() as session:
            r1_id, r2_id = sorted((rect1_id, rect2_id))

            result = await session.execute(
                select(RectangleIntersectionOrm).where(
                    and_(
                        RectangleIntersectionOrm.rectangle1_id == r1_id,
                        RectangleIntersectionOrm.rectangle2_id == r2_id
                    )
                )
            )
            existing = result.scalar_one_or_none()
            if existing:
                return existing.intersection_area

            rects = await session.execute(
                select(RectangleOrm).where(RectangleOrm.id.in_([r1_id, r2_id]))
            )
            rect_list = rects.scalars().all()
            if len(rect_list) < 2:
                return None

            r1, r2 = rect_list

            area = cls._calculate_intersection_area(r1, r2)
            if area is None:
                return None

            inter = RectangleIntersectionOrm(
                rectangle1_id=r1_id,
                rectangle2_id=r2_id,
                intersection_area=area
            )
            session.add(inter)
            await session.commit()
            return area
