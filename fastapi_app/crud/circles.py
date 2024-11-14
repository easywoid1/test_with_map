from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import CircleQuery
from core.schemas import CircleBase


async def get_query(session: AsyncSession, circle: CircleBase) -> CircleQuery | None:
    query = select(CircleQuery).where(
        CircleQuery.latitude == circle.latitude,
        CircleQuery.longitude == circle.longitude,
        CircleQuery.radius == circle.radius,
    )
    cached_result = await session.execute(query)
    result = cached_result.scalar_one_or_none()
    return result


async def create_query(
    session: AsyncSession, circle: CircleBase, geojson_output: dict
) -> CircleQuery | None:
    new_cache_entry = CircleQuery(
        latitude=circle.latitude,
        longitude=circle.longitude,
        radius=circle.radius,
        result=geojson_output,
    )
    session.add(new_cache_entry)
    await session.commit()
    return new_cache_entry