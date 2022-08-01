from typing import List

import geoalchemy2
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models import Zone


async def check_zone_crossing(db: AsyncSession, poly: str):
    result = await db.execute(select(Zone).filter(
        func.ST_Intersects(Zone.zone_coordinates, poly)
    ))
    final = result.scalars().first()
    return final


async def get_zone_for_point(db: AsyncSession, point: geoalchemy2.Geometry("POINT")):
    zone = await db.execute(select(Zone).filter(Zone.zone_coordinates.ST_Contains(point)))
    return zone.scalars().first()
