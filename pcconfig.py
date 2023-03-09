import pynecone as pc
import os


config = pc.Config(
    app_name="tspycher",
    api_url=os.environ.get("API_URL", "http://127.0.0.1:8000"),
    db_url="sqlite:///pynecone.db",
)
