from sqlalchemy import Integer, Float, DateTime, String
from sqlalchemy.schema import Column
from tspycher.database import Base
from pydantic import BaseModel
from datetime import datetime
import uuid


class TeltonikaTrack(Base):
    __tablename__ = "tracks"
    __table_args__ = {'extend_existing': True}

    id: str = Column(String, primary_key=True)

    kmh:float = Column(Float)
    track:float = Column(Float)

    timestamp: datetime = Column(DateTime)
    latitude_decimal_degrees: float = Column(Float)
    latitude_direction: str = Column(String)
    longitude_decimal_degrees: float = Column(Float)
    longitude_direction: str = Column(String)

    altitude:float  = Column(Float)
    num_satellites:int = Column(Integer)
    mobile_imei:int = Column(Integer)
    mobile_serial_num:int = Column(Integer)

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

class TeltonikaTrackSchema(BaseModel):
    id: str = None

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

    class Config:
        orm_mode = True