from fastapi import Request
from tspycher.libs.nmea import parse
import json

async def api_teltonika_gps(imei:int, serial_num:int, request: Request):
    print(f"Received NMEA Data from IMEI: {imei} with Serial Number: {serial_num}")

    payload = await request.body()
    nmea = parse(payload)

    previous = None
    for data in nmea.get_all(aggregate=True):
        if previous:
            if not data.did_geo_change(previous):
                continue
        previous = data
        raw = data.todict()
        raw["imei"] = imei
        raw["serial_num"] = serial_num
        print(f"Data: {json.dumps(raw)}")

    return {"Status": "Received"}