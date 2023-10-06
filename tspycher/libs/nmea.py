import dataclasses
import re
from datetime import datetime, timezone
import logging

logger = logging.getLogger("uvicorn.run")

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
    longitude:float
    timestamp:str
    fix_quality:int
    num_satellites:int
    raw_message:str=None
    altitude:float = None #meters mean sea level

    @property
    def datetime(self) -> datetime:
        return datetime.strptime(self.timestamp, "%H%M%S.%f").replace(tzinfo=timezone.utc, day=datetime.now().day, month=datetime.now().month, year=datetime.now().year)

    @property
    def is_good(self) -> bool:
        return self.fix_quality > 0 and self.fix_quality < 6

    def __str__(self):
        return f"Latitude: {self.latitude_decimal_degrees}, Longitude: {self.longitude_decimal_degrees}, Altitude: {self.altitude}, Datetime: {self.datetime.isoformat()}, Fix Quality: {self.fix_quality}, Number of Satellites: {self.num_satellites}"

@dataclasses.dataclass
class AggregatedTrack:
    kmh:float = None
    track:float = None

    latitude: float = None
    longitude: float = None

    altitude:float  = None #meters mean sea level
    num_satellites:int = None

    timestamp:int = None

    def is_all_data(self) -> bool:
        return self.kmh is not None and \
            self.track is not None and \
            self.latitude is not None and \
            self.timestamp is not None and \
            self.longitude is not None and \
            self.altitude is not None and \
            self.num_satellites is not None


    @property
    def datetime(self) -> datetime:
        return datetime.strptime(self.timestamp, "%H%M%S.%f").replace(tzinfo=timezone.utc, day=datetime.now().day, month=datetime.now().month, year=datetime.now().year)

    def did_geo_change(self, other) -> bool:
        return self.kmh != other.kmh or \
            self.track != other.track or \
            self.latitude != other.latitude or \
            self.longitude != other.longitude or \
            self.altitude != other.altitude

    def __str__(self):
        return f"Latitude: {self.latitude_decimal_degrees}, Longitude: {self.longitude_decimal_degrees}, Datetime: {self.datetime.isoformat()}, Speed: {self.kmh} km/h, Track: {self.track}°, Num Satellites: {self.num_satellites}, Altitude: {self.altitude}"

    def todict(self):
        return {
            "latitude": self.latitude_decimal_degrees,
            "longitude": self.longitude_decimal_degrees,
            "datetime": self.datetime.isoformat(),
            "speed": self.kmh,
            "track": self.track,
            "num_satellites": self.num_satellites,
            "altitude": self.altitude
        }

@dataclasses.dataclass
class NMEA(object):
    sentences:list=None

    def __parse__coord(self, data:str, direction:str) -> float:
        degree = float(data[0:2])
        minutes = float(data[2:]) / 60.0
        if direction.lower() == "s" or direction.lower() == "w":
            return (degree + minutes) * -1

        return degree + minutes

    def __post_init__(self):
        self.sentences = []

    # GPGSA / GAGSA / GNGSA -> Overall Satellite data
    # GPGSV / GLGSV / GAGSV -> Detailed Satellite data
    # GPGGA / GPGGA / GAGGA -> Fix information
    # GNGNS -> ==
    # GPVTG / GAVTG -> Vector track and Speed over the Ground
    # GPRMC / GARMC -> recommended minimum data for gps

    """
    def _parse_gpgsv(self, data:list) -> Fix:
        return self.__parse_gsa(data)

    def _parse_gagsv(self, data: list) -> Fix:
        return self.__parse_gsa(data)

    def _parse_gngsv(self, data: list) -> Fix:
        return self.__parse_gsa(data)

    def _parse_gpgsa(self, data:list) -> Fix:
        return self.__parse_gsa(data)

    def _parse_gagsa(self, data: list) -> Fix:
        return self.__parse_gsa(data)

    def _parse_gngsa(self, data: list) -> Fix:
        return self.__parse_gsa(data)

    def _parse_gsa(self, data:list) -> Fix:
        return Fix(latitude=self.__parse__coord(data[1], data[2]), longitude=self.__parse__coord(data[3], data[4]), altitude=float(data[8]) if data[8] else None, timestamp=data[0], fix_quality=int(data[5]), num_satellites=int(data[6]))
    """

    def _parse_gpgga(self, data:list) -> Fix:
        return Fix(latitude=self.__parse__coord(data[1], data[2]), longitude=self.__parse__coord(data[3], data[4]), altitude=float(data[8]) if data[8] else None, timestamp=data[0], fix_quality=int(data[5]), num_satellites=int(data[6]))

    def _parse_gngga(self, data:list) -> Fix:
        return Fix(latitude=self.__parse__coord(data[1], data[2]), longitude=self.__parse__coord(data[3], data[4]), altitude=float(data[8]) if data[8] else None, timestamp=data[0], fix_quality=int(data[5]), num_satellites=int(data[6]))


    def _parse_gpvtg(self, data:list) -> Vector:
        return Vector(kmh=float(data[4]), track=float(data[2]))

    """
    def _parse_gprmc(self, data:list) -> Track:
        return Track(time=data[0], date=data[8], latitude=self.__parse__coord(data[2], data[3]), longitude=self.__parse__coord(data[4], data[5]), kmh=float(data[6]), track=float(data[7]) if data[7] else 0.0, fix_quality=data[11])
    """

    def get_fixes(self):
        sentences = list(filter(lambda s: s.address == "GPGGA", self.sentences))
        return map(lambda f: self.__parse_gpgga(f.data), sentences)
        #return map(lambda f: Fix(latitude=float(f.data[1]), latitude_direction=f.data[2], longitude=float(f.data[3]), longitude_direction=f.data[4], altitude=float(f.data[8]), timestamp=f.data[0], fix_quality=int(f.data[5]), num_satellites=int(f.data[6]), raw_message=f.raw), sentences)

    def get_vectors(self):
        sentences = list(filter(lambda s: s.address == "GPVTG", self.sentences))
        return map(lambda v: self.__parse_gpvtg(v.data), sentences)
        #return map(lambda s: Vector(kmh=float(s.data[4]), track=float(s.data[2])), sentences)


    def get_all(self, aggregate:bool=False):
        if aggregate:
            known_sentences = []

            a = AggregatedTrack()
            for s in self.sentences:
                logger.debug(f"Parsing Sentence: {s.raw}")
                method = getattr(self, f"_parse_{s.address.strip().lower()}", None)

                if not s.address in known_sentences:
                    known_sentences.append(s.address)

                if not method:
                    logger.debug(f"No parser found for {s.address}")
                    continue

                d = method(s.data)
                if isinstance(d, Fix):
                    a.altitude = d.altitude
                    a.num_satellites = d.num_satellites
                    a.latitude = d.latitude
                    a.longitude = d.longitude
                    a.timestamp = d.timestamp
                elif isinstance(d, Vector):
                    a.kmh = d.kmh
                    a.track = d.track
                else:
                    logger.warning(f"Unknown NMEA final datatype: {type(d)}")
                    continue

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