from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import CoordinatesQuery
from core.schemas import CoordinatesBase


async def get_query(
    session: AsyncSession, coordinates: CoordinatesBase
) -> CoordinatesQuery | None:
    """
    Get coordinates of circle from database
    :param session: session of connection with database
    :param coordinates: coordinates obj with params of circle
    :type coordinates: CoordinatesQuery
    """
    query = select(CoordinatesQuery).where(
        CoordinatesQuery.latitude == coordinates.latitude,
        CoordinatesQuery.longitude == coordinates.longitude,
        CoordinatesQuery.radius == coordinates.radius,
    )
    cached_result = await session.execute(query)
    result = cached_result.scalar_one_or_none()
    return result


async def create_query(
    session: AsyncSession, coordinates: CoordinatesBase, geojson_output: dict
) -> CoordinatesQuery | None:
    """
        Get coordinates of circle from database
        :param session: session of connection with database
        :param coordinates: coordinates obj with params of circle
        :return geojson (json) file with coordinates of circle
        """
    new_cache_entry = CoordinatesQuery(
        latitude=coordinates.latitude,
        longitude=coordinates.longitude,
        radius=coordinates.radius,
        result=geojson_output,
    )
    session.add(new_cache_entry)
    await session.commit()
    return new_cache_entry
