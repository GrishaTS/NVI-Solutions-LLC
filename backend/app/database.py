from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from app.config import settings

engine = create_async_engine(settings.POSTGRES_URL)
new_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Model(DeclarativeBase):
    ...


class RectangleOrm(Model):
    __tablename__ = 'rectangles'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    x1: Mapped[float]
    y1: Mapped[float]
    x2: Mapped[float]
    y2: Mapped[float]



class RectangleIntersectionOrm(Model):
    __tablename__ = 'rectangle_intersections'
    
    id: Mapped[int] = mapped_column(primary_key=True)

    rectangle1_id: Mapped[int] = mapped_column(ForeignKey('rectangles.id'))
    rectangle2_id: Mapped[int] = mapped_column(ForeignKey('rectangles.id'))
    intersection_area: Mapped[float]

    rectangle1: Mapped['RectangleOrm'] = relationship(
        foreign_keys=[rectangle1_id], backref='as_first'
    )
    rectangle2: Mapped['RectangleOrm'] = relationship(
        foreign_keys=[rectangle2_id], backref='as_second'
    )


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)

async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)