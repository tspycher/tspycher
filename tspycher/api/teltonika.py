import uuid
from fastapi import Request, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from tspycher.libs.nmea import parse
from sqlalchemy import Column, ForeignKey, Integer, String, Float
import sqlalchemy
import uuid
from tspycher.database import get_db, Base


class TeltonikaTrack(Base):
    __tablename__ = "tracks"

    id: str = Column(String, primary_key=True)

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

    def todict(self):
        age = datetime.now() - self.timestamp
        is_recent = age.total_seconds() < 60
        return {
            "latitude": self.latitude_decimal_degrees,
            "latitude_direction": self.latitude_direction,
            "longitude": self.longitude_decimal_degrees,
            "longitude_direction": self.longitude_direction,
            "datetime": self.timestamp.isoformat(),
            "is_recent": is_recent,
            "age_seconds": int(age.total_seconds()),
            "speed": self.kmh,
            "track": self.track,
            "num_satellites": self.num_satellites,
            "altitude": self.altitude
        }
metadata = sqlalchemy.MetaData()

notes = sqlalchemy.Table(
    "tracks",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.String, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column("completed", sqlalchemy.Boolean),
)

async def api_teltonika_latest(request: Request, db: Session = Depends(get_db)):
    """with rx.session() as session:
        tracks = session.query(TeltonikaTrack).order_by(TeltonikaTrack.timestamp.desc()).limit(1).all()
        if tracks:
            return tracks[0].todict()
        else:
            return {}
    """
    return {}


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
        print(f"Received NMEA Data: {data.datetime} {data.latitude_decimal_degrees} {data.latitude_direction} {data.longitude_decimal_degrees} {data.longitude_direction} {data.kmh} {data.track} {data.num_satellites} {data.altitude}")
        teltonika_tracks.append(TeltonikaTrack(timestamp=data.datetime,
                       latitude_decimal_degrees=data.latitude_decimal_degrees, latitude_direction=data.latitude_direction,
                       longitude_decimal_degrees=data.longitude_decimal_degrees, longitude_direction=data.longitude_direction,
                       kmh=data.kmh,
                       track=data.track,
                       num_satellites=data.num_satellites,
                       altitude=data.altitude,
                       mobile_imei=imei,
                       mobile_serial_num=serial_num))

    """
    with rx.session() as session:
        session.bulk_save_objects(teltonika_tracks)
        session.commit()
    """

    return {"Status": "Received"}