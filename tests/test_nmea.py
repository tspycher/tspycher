import os
from fastapi.testclient import TestClient
from tspycher.main import app

client = TestClient(app)

testpayload_file = os.path.join(os.path.dirname(__file__), "testpayloadv2.txt")
testpayload = open(testpayload_file, "rb").read()


def test_tracker_latest():
    response = client.get("/api/teltonika/latest")
    data = response.json()
    assert response.status_code == 200
    assert data['id']

def test_tracker():
    response = client.post("/api/teltonika/", params={"imei": 123456789012345, "serial_num": 123456789012345}, data=testpayload)
    data = response.json()
    assert response.status_code == 200
    assert data.get("status") == "Received"
