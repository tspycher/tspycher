async def api_status():
    return {
        "status": "running",
    }

from .airfield import api_airfield
from .teltonika import api_teltonika_gps