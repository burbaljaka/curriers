from typing import List, Union, Optional

from fastapi import FastAPI, Depends, HTTPException
import databases
from fastapi.responses import ORJSONResponse

from sqlalchemy.ext.asyncio import AsyncSession

import serializers
import db_actions

from database import SQLALCHEMY_DATABASE_URL, get_db
from validators import check_zone_crossing


app = FastAPI()


database = databases.Database(SQLALCHEMY_DATABASE_URL)


@app.get("/zones/", response_model=List[Optional[serializers.ZoneReturn]])
async def get_all_zones(db: AsyncSession = Depends(get_db)):
    zones = await db_actions.get_zones(db)
    return zones


@app.post("/zones/", response_model=Union[serializers.ZoneReturn, None])
async def create_new_zone(zone: serializers.ZoneCreate, db: AsyncSession = Depends(get_db)):
    is_valid = await check_zone_crossing(db, zone.zone_coordinates)
    if is_valid is not None:
        raise HTTPException(400, "There is a zones overlapping")
    zone = await db_actions.create_zone(db, zone)
    return zone


@app.post("/get_currier/", response_class=ORJSONResponse)
async def get_currier_for_point(point: serializers.Point, db: AsyncSession = Depends(get_db)):
    currier_id = await db_actions.get_currier_by_point(db, point)
    return {"currier_id": currier_id}


@app.post("/assign_currier/", response_model=Optional[serializers.ZoneReturn])
async def assign_currier_to_zone(data: serializers.ZoneToAssign, db: AsyncSession = Depends(get_db)):
    zone = await db_actions.assign_zone_to_currier(db, data)
    if zone:
        return zone
    else:
        raise HTTPException(400, f"There is no zone with id={data.zone_id}")


@app.post("/seed_db/", response_class=ORJSONResponse)
async def seed_the_db_with_initial_data(db: AsyncSession = Depends(get_db)):
    """
    that works if no intersects found in the db
    """
    result = await db_actions.seeding_data(db)
    return {"result": f"Database was seeded with {result} zones"}
