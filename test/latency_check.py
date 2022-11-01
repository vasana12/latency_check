import requests
url = "http://127.0.0.1:8000/pi"
for i in range(0, 100):
    requests.get(url=url)