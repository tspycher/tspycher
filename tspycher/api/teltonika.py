from fastapi import Request, Depends, APIRouter
from fastapi.responses import StreamingResponse

from sqlalchemy.orm import Session
from tspycher.libs.nmea import parse
from tspycher.database import get_db
from tspycher.api.models.track import TeltonikaTrack, TeltonikaTrackSchema
import logging
from io import StringIO
from pydantic import BaseModel
import simplekml


logger = logging.getLogger("uvicorn.run")

router = APIRouter(
    prefix="/teltonika",
    tags=["Teltonika"],
    responses={404: {"description": "Not found"}}
)

class NmeaResponseSchema(BaseModel):
    status: str
    points_added: int = 0

@router.get("/latest", response_model=TeltonikaTrackSchema)
async def api_teltonika_latest(request: Request, db: Session = Depends(get_db)):
    result = db.query(TeltonikaTrack).order_by(TeltonikaTrack.timestamp.desc()).limit(1).first()
    return result

@router.post("/", response_model=NmeaResponseSchema)
async def api_teltonika_gps(imei:int, serial_num:int, request: Request, db: Session = Depends(get_db)):
    logger.info(f"Received NMEA Data from IMEI: {imei} with Serial Number: {serial_num}")

    payload = await request.body()
    nmea = parse(payload)

    previous = None
    teltonika_tracks = []
    for data in nmea.get_all(aggregate=True):
        if previous:
            if not data.did_geo_change(previous):
                continue
        previous = data
        logger.info(f"Received NMEA Data: {data.datetime} {data.latitude_decimal_degrees} {data.latitude_direction} {data.longitude_decimal_degrees} {data.longitude_direction} {data.kmh} {data.track} {data.num_satellites} {data.altitude}")
        teltonika_tracks.append(TeltonikaTrack(timestamp=data.datetime,
                       latitude_decimal_degrees=data.latitude_decimal_degrees, latitude_direction=data.latitude_direction,
                       longitude_decimal_degrees=data.longitude_decimal_degrees, longitude_direction=data.longitude_direction,
                       kmh=data.kmh,
                       track=data.track,
                       num_satellites=data.num_satellites,
                       altitude=data.altitude,
                       mobile_imei=imei,
                       mobile_serial_num=serial_num))

    
    db.add_all(teltonika_tracks)
    db.commit()

    return {"status": "Received", "points_added": len(teltonika_tracks)}


@router.get("/kml", response_model=TeltonikaTrackSchema)
async def api_teltonika_latest(waypoints:int=100, db: Session = Depends(get_db)):
    kml = simplekml.Kml()
    ls = kml.newlinestring(name='Defender Teltonika Tracks')
    ls.extrude = 0
    for track in db.query(TeltonikaTrack).order_by(TeltonikaTrack.timestamp.desc()).limit(waypoints).all():
        ls.coords.addcoordinates([(track.longitude_decimal_degrees, track.latitude_decimal_degrees, track.altitude)])
    ls.altitudemode = simplekml.AltitudeMode.clamptoground
    ls.style.linestyle.width = 2
    ls.style.linestyle.color = simplekml.Color.blue

    result = StringIO()
    result.write(kml.kml())
    result.seek(0)

    return StreamingResponse(result, media_type='application/vnd.google-earth.kml+xml')