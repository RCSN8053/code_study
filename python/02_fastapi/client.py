import requests

respons = requests.get("http://127.0.0.1:8000/health")
print(respons.json())
respons = requests.get("http://127.0.0.1:8000/hello/ASD")
print(respons.json())
respons = requests.get("http://127.0.0.1:8000/greet?name=ASD")
print(respons.json())
respons = requests.post("http://127.0.0.1:8000/welcome", json= {"name": "ASD"})
print(respons.json())