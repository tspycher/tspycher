import os

if os.path.exists(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "credentials.json"))):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "credentials.json"))

from .state import State
from .tspycher import app