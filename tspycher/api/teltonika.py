import uuid

import reflex as rx
from fastapi import Request
from datetime import datetime
from tspycher.libs.nmea import parse
import sqlmodel
import uuid

class TeltonikaTrack(rx.Model, table=True):
    __tablename__ = "tracks"

    id: str = sqlmodel.Field(primary_key=True)

    kmh:float = None
    track:float = None

    timestamp: datetime = None
    latitude_decimal_degrees: float = None
    latitude_direction: str = None
    longitude_decimal_degrees: float = None
    longitude_direction: str = None

    altitude:float  = None
    num_satellites:int = None
    mobile_imei:int = None
    mobile_serial_num:int = None

    def __init__(self, **kwargs):
        self.id = str(uuid.uuid4())
        super().__init__(**kwargs)

async def api_teltonika_gps(imei:int, serial_num:int, request: Request):
    print(f"Received NMEA Data from IMEI: {imei} with Serial Number: {serial_num}")

    payload = await request.body()
    nmea = parse(payload)

    previous = None
    teltonika_tracks = []
    for data in nmea.get_all(aggregate=True):
        if previous:
            if not data.did_geo_change(previous):
                continue
        previous = data
        teltonika_tracks.append(TeltonikaTrack(timestamp=data.datetime,
                       latitude_decimal_degrees=data.latitude_decimal_degrees, latitude_direction=data.latitude_direction,
                       longitude_decimal_degrees=data.longitude_decimal_degrees, longitude_direction=data.longitude_direction,
                       kmh=data.kmh,
                       track=data.track,
                       num_satellites=data.num_satellites,
                       altitude=data.altitude,
                       mobile_imei=imei,
                       mobile_serial_num=serial_num))

    with rx.session() as session:
        session.bulk_save_objects(teltonika_tracks)
        session.commit()

    return {"Status": "Received"}