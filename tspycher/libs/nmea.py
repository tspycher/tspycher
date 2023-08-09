import dataclasses
import re
from datetime import datetime, timezone

@dataclasses.dataclass
class Vector:
    kmh:float
    track:float

@dataclasses.dataclass
class Fix:
    QUALITY_NOT_AVAILABLE = 0
    QUALITY_SINGLE_POINT = 1
    QUALITY_PSUEDORANGE_DIFFERENTIAL = 2
    QUALITY_RTK_FIXED_AMBIGUITY_SOLUTION = 4
    QUALITY_RTK_FLOATING_AMBIGUITY_SOLUTION = 5
    QUALITY_DEAD_RECKONING_MODE = 6
    QUALITY_MANUAL_INPUT_MODE = 7
    QUALITY_SIMULATOR_MODE = 8
    QUALITY_WAAS = 9
    QUALITY_OMNISTAR = 10
    QUALITY_OMNISTAR_HP = 11
    QUALITY_OMNISTAR_XP = 12
    QUALITY_CDGPS = 13
    QUALITY_NOT_VALID = 14
    QUALITY_INVALID = 15

    latitude:float
    latitude_direction:str
    longitude:float
    longitude_direction:str
    timestamp:str
    fix_quality:int
    num_satellites:int
    raw_message:str=None
    altitude:float = None #meters mean sea level

    @property
    def latitude_decimal_degrees(self) -> float:
        return self.latitude / 100

    @property
    def longitude_decimal_degrees(self) -> float:
        return self.longitude / 100

    @property
    def datetime(self) -> datetime:
        return datetime.strptime(self.timestamp, "%H%M%S.%f").replace(tzinfo=timezone.utc, day=datetime.now().day, month=datetime.now().month, year=datetime.now().year)

    @property
    def is_good(self) -> bool:
        return self.fix_quality > 0 and self.fix_quality < 6

    def __str__(self):
        return f"Latitude: {self.latitude_decimal_degrees} {self.latitude_direction}, Longitude: {self.longitude_decimal_degrees} {self.longitude_direction}, Altitude: {self.altitude}, Datetime: {self.datetime.isoformat()}, Fix Quality: {self.fix_quality}, Number of Satellites: {self.num_satellites}"

@dataclasses.dataclass
class Track:
    time: str
    date: str
    latitude: float
    latitude_direction: str
    longitude: float
    longitude_direction: str

    kmh:float
    track:float

    fix_quality: str

    @property
    def latitude_decimal_degrees(self) -> float:
        return self.latitude / 100

    @property
    def longitude_decimal_degrees(self) -> float:
        return self.longitude / 100

    @property
    def datetime(self) -> datetime:
        d = datetime.strptime(self.date, "%d%m%y")
        return datetime.strptime(self.time, "%H%M%S.%f").replace(tzinfo=timezone.utc, day=d.day, month=d.month, year=d.year)

    def __str__(self):
        return f"Latitude: {self.latitude_decimal_degrees} {self.latitude_direction}, Longitude: {self.longitude_decimal_degrees} {self.longitude_direction}, Datetime: {self.datetime.isoformat()}, Speed: {self.kmh} km/h, Track: {self.track}°, Fix Quality: {self.fix_quality}"


@dataclasses.dataclass
class AggregatedTrack:
    kmh:float = None
    track:float = None

    time: str = None
    date: str = None
    latitude: float = None
    latitude_direction: str = None
    longitude: float = None
    longitude_direction: str = None

    altitude:float  = None #meters mean sea level
    num_satellites:int = None

    def is_all_data(self) -> bool:
        return self.kmh is not None and \
            self.track is not None and \
            self.time is not None and \
            self.date is not None and \
            self.latitude is not None and \
            self.latitude_direction is not None and \
            self.longitude is not None and \
            self.longitude_direction is not None and \
            self.altitude is not None and \
            self.num_satellites is not None

    @property
    def latitude_decimal_degrees(self) -> float:
        return self.latitude / 100

    @property
    def longitude_decimal_degrees(self) -> float:
        return self.longitude / 100

    @property
    def datetime(self) -> datetime:
        d = datetime.strptime(self.date, "%d%m%y")
        return datetime.strptime(self.time, "%H%M%S.%f").replace(tzinfo=timezone.utc, day=d.day, month=d.month, year=d.year)

    def did_geo_change(self, other) -> bool:
        return self.kmh != other.kmh or \
            self.track != other.track or \
            self.latitude != other.latitude or \
            self.latitude_direction != other.latitude_direction or \
            self.longitude != other.longitude or \
            self.longitude_direction != other.longitude_direction or \
            self.altitude != other.altitude

    def __str__(self):
        return f"Latitude: {self.latitude_decimal_degrees} {self.latitude_direction}, Longitude: {self.longitude_decimal_degrees} {self.longitude_direction}, Datetime: {self.datetime.isoformat()}, Speed: {self.kmh} km/h, Track: {self.track}°, Num Satellites: {self.num_satellites}, Altitude: {self.altitude}"

    def todict(self):
        return {
            "latitude": self.latitude_decimal_degrees,
            "latitude_direction": self.latitude_direction,
            "longitude": self.longitude_decimal_degrees,
            "longitude_direction": self.longitude_direction,
            "datetime": self.datetime.isoformat(),
            "speed": self.kmh,
            "track": self.track,
            "num_satellites": self.num_satellites,
            "altitude": self.altitude
        }

@dataclasses.dataclass
class NMEA:
    sentences:list=None

    def __post_init__(self):
        self.sentences = []

    def __parse_gpgga(self, data:list) -> Fix:
        return Fix(latitude=float(data[1]), latitude_direction=data[2], longitude=float(data[3]), longitude_direction=data[4], altitude=float(data[8]) if data[8] else None, timestamp=data[0], fix_quality=int(data[5]), num_satellites=int(data[6]))

    def __parse_gpvtg(self, data:list) -> Vector:
        return Vector(kmh=float(data[4]), track=float(data[2]))

    def __parse_gprmc(self, data:list) -> Track:
        return Track(time=data[0], date=data[8], latitude=float(data[2]), latitude_direction=data[3], longitude=float(data[4]), longitude_direction=data[5], kmh=float(data[6]), track=float(data[7]) if data[7] else 0.0, fix_quality=data[11])

    def get_fixes(self):
        sentences = list(filter(lambda s: s.address == "GPGGA", self.sentences))
        return map(lambda f: self.__parse_gpgga(f.data), sentences)
        #return map(lambda f: Fix(latitude=float(f.data[1]), latitude_direction=f.data[2], longitude=float(f.data[3]), longitude_direction=f.data[4], altitude=float(f.data[8]), timestamp=f.data[0], fix_quality=int(f.data[5]), num_satellites=int(f.data[6]), raw_message=f.raw), sentences)

    def get_vectors(self):
        sentences = list(filter(lambda s: s.address == "GPVTG", self.sentences))
        return map(lambda v: self.__parse_gpvtg(v.data), sentences)
        #return map(lambda s: Vector(kmh=float(s.data[4]), track=float(s.data[2])), sentences)

    def get_track(self):
        sentences = list(filter(lambda s: s.address == "GPRMC", self.sentences))
        return map(lambda t: self.__parse_gprmc(t.data), sentences)
        #return map(lambda t: Track(time=t.data[0], date=t.data[8], latitude=float(t.data[2]), latitude_direction=t.data[3], longitude=float(t.data[4]), longitude_direction=t.data[5], kmh=float(t.data[6]), track=float(t.data[7]) if t.data[7] else 0.0, fix_quality=t.data[11]), sentences)

    def get_all(self, aggregate:bool=False):
        if aggregate:
            a = AggregatedTrack()
            for s in self.sentences:
                if s.address == "GPGGA":
                    d = self.__parse_gpgga(s.data)
                    a.altitude = d.altitude
                    a.num_satellites = d.num_satellites
                    a.latitude = d.latitude
                    a.latitude_direction = d.latitude_direction
                    a.longitude = d.longitude
                    a.longitude_direction = d.longitude_direction
                    a.time = d.timestamp
                elif s.address == "GPVTG":
                    d = self.__parse_gpvtg(s.data)
                    a.kmh = d.kmh
                    a.track = d.track
                elif s.address == "GPRMC":
                    d = self.__parse_gprmc(s.data)
                    a.time = d.time
                    a.date = d.date
                    a.latitude = d.latitude
                    a.latitude_direction = d.latitude_direction
                    a.longitude = d.longitude
                    a.longitude_direction = d.longitude_direction
                    a.kmh = d.kmh
                    a.track = d.track

                if a.is_all_data():
                    yield a
            return

        for s in self.sentences:
            if s.address == "GPGGA":
                yield self.__parse_gpgga(s.data)
            elif s.address == "GPVTG":
                yield self.__parse_gpvtg(s.data)
            elif s.address == "GPRMC":
                yield self.__parse_gprmc(s.data)


@dataclasses.dataclass
class Sentence:
    address:str
    data:list
    checksum:int
    raw:str


def parse(payload:bytes) -> NMEA:
    nmea = NMEA()
    for l in payload.decode("utf-8").split("\n"):
        m = re.search(r'((?<=\$)[A-Z]{5}),(.*(?=\*))\*([A-Z0-9]{2})', l, re.M)
        if not m:
            continue
        s = Sentence(address=m.group(1), data=m.group(2).split(","), checksum=m.group(3), raw=l)
        nmea.sentences.append(s)
    return nmea