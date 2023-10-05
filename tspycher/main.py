from fastapi import FastAPI, APIRouter

app = FastAPI(
    title="tspycher API",
    description="api's for my Life",
    root_path="/api",
)
router = APIRouter(
    prefix="/api",
    tags=["Api"],
    responses={404: {"description": "Not found"}}
)



#from tspycher.api import api_airfield, api_teltonika_gps, api_teltonika_latest
from tspycher.api import api_airfield


@router.get("/")
def read_root():
    return {"Hello": "World"}


#app.add_api_route("/teltonika", api_teltonika_gps, methods=["POST"])
#app.add_api_route("/teltonika/latest", api_teltonika_latest, methods=["GET"])
router.add_api_route("/airfield/{name}", api_airfield)

app.include_router(router)