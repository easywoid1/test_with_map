import numpy as np
from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from shapely.geometry import Polygon
import pyproj
import geopandas as gpd

from crud.coordinates import create_query, get_query
from core.models import db_helper
from core.schemas.coordinates import CoordinatesBase
import asyncio
from functools import partial

router = APIRouter(tags=["Circles"], prefix="/circles")


async def async_calculate_polygon(circle: CoordinatesBase) -> Any:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, partial(_calculate_polygon_sync, circle))


def _calculate_polygon_sync(coordinates: CoordinatesBase) -> Any:
    proj = pyproj.Proj(
        proj="utm", zone=int((coordinates.longitude + 180) // 6) + 1, ellps="WGS84"
    )

    # Оптимизируем работу с numpy
    x, y = proj(coordinates.longitude, coordinates.latitude)
    angles = np.linspace(0, 2 * np.pi, 30, dtype=np.float32)
    circle_x = x + coordinates.radius * np.cos(angles)
    circle_y = y + coordinates.radius * np.sin(angles)

    lon_circle, lat_circle = proj(circle_x, circle_y, inverse=True)
    polygon = Polygon(zip(lon_circle, lat_circle))

    return gpd.GeoDataFrame({"geometry": [polygon]}, crs="EPSG:4326").to_json()


@router.post("/")
async def get_polygon(
    circle: CoordinatesBase, session: AsyncSession = Depends(db_helper.session_getter)
) -> dict:
    """
    Неблокирующий эндпоинт для получения полигона.

    :param circle: Объект круга с координатами и радиусом для встроенной валидации pydantic
    :param session: асинхронная сессия БД
    :return: GeoJSON с замкнутым кругом
    """
    try:
        # Проверяем кэш
        result = await get_query(session=session, coordinates=circle)

        if result:
            return {"result": result.result}

        await asyncio.sleep(10)
        geojson_output = await async_calculate_polygon(circle)

        # Кешируем запрос
        await create_query(session, circle, geojson_output=geojson_output)

        return {"result": geojson_output}

    except Exception as e:
        await session.rollback()
        return {"error": f"Error processing request: {str(e)}"}
