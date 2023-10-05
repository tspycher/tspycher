from fastapi import FastAPI

app = FastAPI()

#from tspycher.api import api_airfield, api_teltonika_gps, api_teltonika_latest
from tspycher.api import api_airfield


@app.get("/")
def read_root():
    return {"Hello": "World"}


#app.add_api_route("/teltonika", api_teltonika_gps, methods=["POST"])
#app.add_api_route("/teltonika/latest", api_teltonika_latest, methods=["GET"])
app.add_api_route("/airfield/{name}", api_airfield)
