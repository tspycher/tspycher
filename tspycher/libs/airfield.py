import requests
from bs4 import BeautifulSoup
import re
import time
import hmac
import hashlib
import math
import os


try:
    from lxml import etree

    lxml_available = True
except:
    lxml_available = False

metar_url = "https://aviationweather.gov/adds/dataserver_current/current/metars.cache.xml"

configs = {
    "lszi": {
        "roundshot_name": "flugplatzschupfart",
        "altitude": 1788,
        "runway": 70,
        "roundshot_image_type": "full3",
        "weatherlink_api_key": os.environ.get("WEATHERLINK_API_KEY"),
        "weatherlink_api_secret": os.environ.get("WEATHERLINK_API_SECRET"),
        "weatherlink_station_id": 10986,
        "website": "https://www.aecs-fricktal.ch/piloten",
        "metar_stations": ["lfsb", "lszh", "lsgs", "lszb", "lszl"]
    }
}


class Airfield(object):
    config = None

    def __init__(self, config: dict) -> None:
        super().__init__()
        self.config = config

    def get_metar(self) -> dict:
        result = {}
        if not self.config.get("metar_stations") and lxml_available:
            return result

        try:
            r = requests.get(metar_url)
            r.raise_for_status()

            root = etree.fromstring(r.content)
            for s in self.config.get("metar_stations"):
                metar = root.xpath(f'/response/data/METAR[station_id="{s.upper()}"]/raw_text').pop()
                result[s.lower()] = metar.text
        except Exception as e:
            print(f"Error: {e}")
            return {}

        return result

    def get_weather(self) -> dict:
        if not self.config.get('weatherlink_api_key') or not self.config.get('weatherlink_api_secret'):
            return {"error": "no weatherlink api key/secret provided"}

        full_record = {}
        api_time = int(time.time())

        station_id = None
        if not self.config.get("weatherlink_station_id"):
            x = f"api-key{self.config.get('weatherlink_api_key')}t{api_time}"
            signature = hmac.new(self.config.get('weatherlink_api_secret').encode(), msg=x.encode(),
                                 digestmod=hashlib.sha256).hexdigest()

            url = "https://api.weatherlink.com/v2/stations"
            r = requests.get(url, params={"api-key": self.config.get('weatherlink_api_key'), "t": api_time,
                                          "api-signature": signature})
            station_id = r.json().get("stations")[0].get("station_id")
        else:
            station_id = self.config.get("weatherlink_station_id")

        #for station in r.json().get("stations"):
        x = f"api-key{self.config.get('weatherlink_api_key')}station-id{station_id}t{api_time}"
        signature = hmac.new(self.config.get('weatherlink_api_secret').encode(), msg=x.encode(),
                             digestmod=hashlib.sha256).hexdigest()

        url = f"https://api.weatherlink.com/v2/current/{station_id}"

        r2 = requests.get(url, params={"api-key": self.config.get('weatherlink_api_key'), "t": api_time,
                                       "api-signature": signature})

        full_record["data"] = r2.json().get("sensors")[0].get("data")[0]

        oat = (full_record["data"]["temp_out"] - 32) * .5556
        dew = (full_record["data"]["dew_point"] - 32) * .5556
        hpa = full_record["data"]["bar"] * 33.86388640341
        alt_m = self.config.get("altitude") * 0.3048
        hpa_msl = hpa + ((hpa * 9.80665 * alt_m) / (287 * (273 + oat + (alt_m / 400))))

        windspeed_kmh = full_record["data"].get("wind_speed") * 1.609344
        crosswind_factor = math.fabs(full_record["data"].get("wind_dir") - self.config.get("runway")) % 180.0
        crosswind_component = windspeed_kmh / 90.0 * crosswind_factor
        crosswind_percent = 1.0 / 90.0 * crosswind_factor

        pressure_altitude = round((29.92 - full_record["data"]["bar"]) * 1000 + self.config.get("altitude"), 0)
        standard_temperature = ((self.config.get("altitude") / 1000 * 2) - 15) * -1
        density_altitude = round(pressure_altitude + (120 * (oat - standard_temperature)), 0)
        spread = round(full_record["data"]["temp_out"] - full_record["data"]["dew_point"], 2)
        cloud_base = round(self.config.get("altitude") + spread / 4.4 * 1000, 0)

        full_record["calculations"] = {
            "oat": round(oat, 1),
            "altitude": self.config.get("altitude"),
            "pressure_altitude": int(pressure_altitude),
            "density_altitude": int(density_altitude),
            "spread": spread,
            "cloud_base": int(cloud_base),
            "crosswind_factor": crosswind_factor,
            "crosswind_component": crosswind_component,
            "crosswind_percent": int(round(crosswind_percent * 100, 0))
        }

        full_record["normalized"] = {
            "oat": round(oat, 1),
            "wind_speed": round(windspeed_kmh, 1),
            "wind_speed_10_min_avg": round(full_record["data"].get("wind_speed_10_min_avg") * 1.609344, 1),
            "wind_gust_10_min": round(full_record["data"].get("wind_gust_10_min") * 1.609344, 1),
            "wind_dir": full_record["data"].get("wind_dir"),
            "pressure": int(round(hpa, 0)),
            "pressure_msl": int(round(hpa_msl, 0)),
            "humidity": full_record["data"].get("hum_out"),
            "rain_rate_mm": full_record["data"].get("rain_rate_mm"),
            "dew_point": round(dew, 1),
        }

        return full_record

    def get_runway_status(self) -> int:
        if not self.config.get('website'):
            return 9
        try:
            r = requests.get(self.config.get('website'))
            r.raise_for_status()
            payload = r.text
            soup = BeautifulSoup(payload, features="html.parser")
            result = soup.find_all("div", {"class": "dashboardLabelPisteMain"}).pop()
            result2 = result.find_all("div", {"class": "dashboardLabelPisteLevel"}).pop()
            value = result2.text
            match = re.search(r'\d{1}', value, re.M)
            if not match:
                raise Exception("Regex not found")
            return int(match[0])
        except Exception as e:
            print(e)
            return 9

    def get_latest_image_url(self) -> str:
        try:
            r = requests.get(f"https://{self.config.get('roundshot_name')}.roundshot.co/structure.json")
            r.raise_for_status()
            image = r.json().get("images")[0]
            return image.get("structure").get(self.config.get('roundshot_image_type')).get("url_full")
        except Exception as e:
            print(e)
            return None