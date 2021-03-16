#unit test for API connection
import requests
def api():
    response = requests.get("http://localhost:5000/api/test")
    assert response.status_code == 200



