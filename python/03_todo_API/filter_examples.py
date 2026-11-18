from fastapi.testclient import TestClient
from main import app, TODOS

client = TestClient(app)
TODOS.clear()

for text in ["산책", "복습", "정리"]:
    client.post("/todos", json={"text": text})

first = client.get("/todos").json()[0]
client.put("/todos/" + str(first["id"]), json={"text": first["text"], "done": True})

for status in ["all", "done", "pending"]:
    response = client.get("/todos", params={"status": status})
    print(status, response.status_code, len(response.json()))

response = client.get("/todos", params={"status": "other"})
print("other", response.status_code)