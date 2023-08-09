from tspycher import app
from fastapi.testclient import TestClient

app.__config__.db_config = "sqlite:///reflex_unittest.db"
client = TestClient(app.api)