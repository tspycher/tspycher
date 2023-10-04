from tspycher import app
from fastapi.testclient import TestClient
from reflex.reflex import db_init, makemigrations, migrate

app.__config__.db_config = "sqlite:///reflex_unittest.db"
#makemigrations()
#migrate()
client = TestClient(app.api)