import pynecone as pc
import os

if os.environ.get("BUN_INSTALL"):
    bun_path = f"{os.environ.get('BUN_INSTALL')}/bin/bun"
else:
    bun_path = pc.constants.BUN_PATH

config = pc.Config(
    app_name="tspycher",
    api_url=os.environ.get("API_URL", "http://127.0.0.1:8000"),
    db_url="sqlite:///pynecone.db",
    bun_path=bun_path,
    telemetry_enabled=False
)
