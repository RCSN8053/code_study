from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

response = client.post("/todos", json={"text": "복습"})
print("정상 등록", response.status_code, response.json())

response = client.post("/todos", json={})
print("text 누락", response.status_code)
print(response.json()["detail"][0]["loc"])

response = client.post("/todos", json={"text": ""})
print("빈 문자열", response.status_code, response.json())