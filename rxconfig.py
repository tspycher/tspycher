import reflex as rx
import os

if os.environ.get("BUN_INSTALL"):
    bun_path = f"{os.environ.get('BUN_INSTALL')}/bin/bun"
else:
    bun_path = rx.constants.BUN_PATH

if os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'):
    db_url = f"bigquery://tspycher/{os.environ.get('BIGQUERY_DATASET', 'teltonika_development')}"
else:
    db_url = "sqlite:///reflex.db"

config = rx.Config(
    app_name="tspycher",
    api_url=os.environ.get("API_URL", "http://127.0.0.1:8000"),
    db_url=db_url,
    bun_path=bun_path,
    telemetry_enabled=False
)

