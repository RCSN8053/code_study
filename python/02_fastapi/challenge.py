from fastapi import FastAPI

app = FastAPI()

# @app.get("/format")
# def format(name: str = "손님", prefix : str = "안녕"):
#     return {f"{prefix}, {name}"}

@app.get("/profile")
def profile():
    profile = {"name" : "민수", "interest": "파이썬"}
    return profile

@app.get("/hello/{name}")
def hello(name):
    return {"message": f"{name}님, 안녕하세요"}

@app.get("/repeat")
def repeat(word: str = "안녕", count: int = 1):
    return {"text": word * count}

@app.post("/introduce")
def introduce(data: dict):
    return {
        "message": f"{data['name']}님은 {data['interest']}에 관심이 있습니다"
    }
@app.get("/length/{text}")
def length(text):
    return {"length": len(text)}