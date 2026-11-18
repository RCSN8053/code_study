from fastapi.testclient import TestClient
from main import app, TODOS

client = TestClient(app)


def test_home():
    assert client.get("/").status_code == 200


def test_create_todo():
    TODOS.clear()
    response = client.post("/todos", json={"text": "산책"})
    assert response.status_code == 201
    assert response.json()["text"] == "산책"
    assert response.json()["done"] == False


def test_created_todo_can_be_listed_and_read():
    TODOS.clear()
    todo = client.post("/todos", json={"text": "복습"}).json()
    assert client.get("/todos").json() == [todo]
    assert client.get("/todos/" + str(todo["id"])).json() == todo


def test_unknown_todo_returns_404():
    TODOS.clear()
    assert client.get("/todos/99999").status_code == 404


def test_update_todo():
    TODOS.clear()
    todo = client.post("/todos", json={"text": "복습"}).json()
    response = client.put("/todos/" + str(todo["id"]), json={"text": "복습 완료", "done": True})
    assert response.status_code == 200
    expected = {"id": todo["id"], "text": "복습 완료", "done": True}
    assert response.json() == expected
    assert client.get("/todos/" + str(todo["id"])).json() == expected


def test_delete_todo():
    TODOS.clear()
    todo = client.post("/todos", json={"text": "복습"}).json()
    path = "/todos/" + str(todo["id"])
    assert client.delete(path).status_code == 200
    assert client.get(path).status_code == 404


def test_missing_text_returns_422():
    assert client.post("/todos", json={}).status_code == 422


def test_empty_text_returns_422():
    assert client.post("/todos", json={"text": ""}).status_code == 422