from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func

import features
import seed_data
import serializers
import validators
from models import Zone


async def get_zones(db: AsyncSession):
    data = await db.execute(select(Zone))
    result = data.scalars().all()
    return result


async def create_zone(db: AsyncSession, coordinates: serializers.ZoneCreate) -> serializers.ZoneReturn:
    zone = Zone(zone_coordinates=coordinates.zone_coordinates, currier=coordinates.currier)
    db.add(zone)
    await db.commit()
    await db.refresh(zone)
    return zone


async def get_currier_by_point(db: AsyncSession, point: serializers.Point) -> Optional[int]:
    point_obj = serializers.make_point_obj_from_point(point)
    data = await db.execute(select(Zone).filter(func.ST_Intersects(Zone.zone_coordinates, point_obj)))
    result = data.scalars().first()
    return result.currier if result else None


async def assign_zone_to_currier(db: AsyncSession, data: serializers.ZoneToAssign) -> Optional[serializers.ZoneReturn]:
    zone_results = await db.execute(select(Zone).filter(Zone.id == data.zone_id))
    zone = zone_results.scalars().first()
    if zone:
        zone.currier = data.currier
        db.add(zone)
        await db.commit()
        await db.refresh(zone)
        return zone

    return None


async def seeding_data(db: AsyncSession) -> int:
    list_to_import = seed_data.coords_list
    counter = 0
    for coords in list_to_import:
        poly = features.make_polygon_from_list(coords)
        result = await validators.check_zone_crossing(db, poly)
        if not result:
            zone = Zone(zone_coordinates=poly)
            db.add(zone)
            counter += 1

    await db.commit()
    return counter
