import os
from . import client

testpayload_file = os.path.join(os.path.dirname(__file__), "testpayload.txt")
testpayload = open(testpayload_file, "rb").read()


def test_tracker():
    response = client.post("/teltonika", params={"imei": 123456789012345, "serial_num": 123456789012345}, data=testpayload)
    assert response.status_code == 200
    assert response.json() == {"Status": "Received"}
