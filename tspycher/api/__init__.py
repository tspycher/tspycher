from tspycher.libs import Airfield, airfield_configs

async def api_airfield(name: str):
    airfield = Airfield(config=airfield_configs.get(name))
    return {
        "webcam_image_url": airfield.get_latest_image_url(),
        "runway_status": airfield.get_runway_status(),
        "weather": airfield.get_weather(),
        "metar": airfield.get_metar()
    }

async def api_status():
    return {
        "status": "running",
    }