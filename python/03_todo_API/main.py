from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

TODOS = []

class TodoCreate(BaseModel):
    text: str

class TodoUpdate(BaseModel):
    text: str
    done: bool

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
    todo = {"id": len(TODOS) + 1, "text": data.text, "done": False}
    TODOS.append(todo)
    return todo

@app.get("/todos")
def  list_todo():
    return TODOS

@app.get("/count")
def count_todos():
    return {"count": len(TODOS)}

# @app.get("/todos/{todo_id}")
# def get_todo(todo_id: int):
#     return TODOS[todo_id]

# @app.get("/todos/{todo_id}")
# def get_todo(todo_id: int):
#     for todo in TODOS:
#         if todo["id"] == todo_id:
#             return todo
#     raise HTTPException(status_code=404, detail="할 일을 찾을 수 없습니다")

@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    return find_todo(todo_id)

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
    return {"deleted" : todo_id}