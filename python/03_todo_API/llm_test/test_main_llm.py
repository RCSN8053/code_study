from fastapi.testclient import TestClient
from llm_test.main_llm import app, TODOS

client = TestClient(app)


def test_home():
    assert client.get("/").status_code == 200


def test_create_todo():
    TODOS.clear()
    response = client.post("/todos", json={"text": "산책"})
    assert response.status_code == 201
    todo = response.json()
    assert todo["text"] == "산책"
    assert todo["done"] is False


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


def test_filter_done():
    TODOS.clear()
    first = client.post("/todos", json={"text": "복습"}).json()
    client.post("/todos", json={"text": "산책"})
    client.put("/todos/" + str(first["id"]), json={"text": "복습", "done": True})
    result = client.get("/todos?status=done").json()
    assert len(result) == 1
    assert result[0]["id"] == first["id"]


def test_filter_pending():
    TODOS.clear()
    first = client.post("/todos", json={"text": "복습"}).json()
    second = client.post("/todos", json={"text": "산책"}).json()
    client.put("/todos/" + str(first["id"]), json={"text": "복습", "done": True})
    assert client.get("/todos?status=pending").json() == [second]


def test_unknown_status_returns_400():
    assert client.get("/todos?status=other").status_code == 400