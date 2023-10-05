from fastapi import APIRouter
from tspycher.libs import Airfield, airfield_configs

router = APIRouter(
    prefix="/airfield",
    tags=["Airfield"],
    responses={404: {"description": "Not found"}}
)


@router.get("/{name}")
async def api_airfield(name: str):
    airfield = Airfield(config=airfield_configs.get(name))
    errors = []
    try:
        webcam_image_url = airfield.get_latest_image_url()
    except Exception as e:
        errors.append({
            "module": "webcam_image",
            "class": e.__class__.__name__,
            "details": str(e)
        })
        webcam_image_url = None

    try:
        runway_status = airfield.get_runway_status()
    except Exception as e:
        errors.append({
            "module": "runway_status",
            "class": e.__class__.__name__,
            "details": str(e)
        })
        runway_status = None
    try:
        weather = airfield.get_weather()
    except Exception as e:
        errors.append({
            "module": "weather",
            "class": e.__class__.__name__,
            "details": str(e)
        })
        weather = None

    try:
        metar = airfield.get_metar()
    except Exception as e:
        errors.append({
            "module": "metar",
            "class": e.__class__.__name__,
            "details": str(e)
        })
        metar = None

    payload = {
        "webcam_image_url": webcam_image_url,
        "runway_status": runway_status,
        "weather": weather,
        "metar": metar
    }
    if errors:
        payload["errors"] = errors

    return payload

