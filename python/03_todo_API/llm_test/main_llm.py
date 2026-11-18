from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

class TodoCreate(BaseModel):
    text: str = Field(min_length=1)

class TodoUpdate(BaseModel):
    text: str = Field(min_length=1)
    done: bool

TODOS = []
NEXT_ID = 1

def find_todo(todo_id):
    for todo in TODOS:
        if todo["id"] == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="할 일을 찾을 수 없습니다")

@app.get("/")
def home():
    return {"message": "안녕하세요"}

@app.post("/preview")
def preview(todo: TodoCreate):
    return {"text": todo.text}

@app.post("/todos", status_code=201)
def create_todo(data: TodoCreate):
    global NEXT_ID
    todo = {"id": NEXT_ID, "text": data.text, "done": False}
    NEXT_ID += 1
    TODOS.append(todo)
    return todo

@app.get("/todos")
def list_todos(status: str = "all"):
    if status not in ("all", "done", "pending"):
        raise HTTPException(
            status_code=400,
            detail="status는 all, done, pending 중 하나여야 합니다"
        )
    if status == "done":
        return [todo for todo in TODOS if todo["done"]]
    elif status == "pending":
        return [todo for todo in TODOS if not todo["done"]]
    return TODOS

@app.get("/count")
def count_todos():
    return {"count": len(TODOS)}

@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    return find_todo(todo_id)

@app.get("/todos/{todo_id}/text")
def get_todo_text(todo_id: int):
    todo = find_todo(todo_id)
    return {"text": todo["text"]}

@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, data: TodoUpdate):
    todo = find_todo(todo_id)
    todo["text"] = data.text
    todo["done"] = data.done
    return todo

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    todo = find_todo(todo_id)
    TODOS.remove(todo)
    return {"deleted": todo_id}

@app.put("/todos/{todo_id}/done")
def mark_done(todo_id: int):
    todo = find_todo(todo_id)
    todo["done"] = True
    return todo