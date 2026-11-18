from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

BOOKS = []
NEXT_ID = 1

# 등록에 쓸 모델과 수정에 쓸 모델을 만든다.

# 번호로 책을 찾는 함수를 만든다. 없으면 404로 답한다.

# 등록, 목록, 한 권 조회, 수정, 삭제 경로를 만든다.
'''
1. 규칙 표를 보고 각 요청의 본문과 기대 응답을 먼저 문서로 정리한다.
`{"title":"파이썬 입문","pages":320}`을 등록했을 때의 응답부터 적어 본다.

2. `test_reading_api.py`에 아래 일곱 경우를 테스트로 쓴다.
6교시의 `test_main.py`를 본보기로 삼되, 테스트마다 `BOOKS.clear()`로 시작하고 필요한 책을 직접 등록해 응답의 `id`를 사용한다.

3. 구현하기 전에 `pytest test_reading_api.py`를 실행해 일곱 개가 모두 실패하는 것을 확인한다.

4. `reading_api.py`의 주석 자리에 모델, 검색 함수, 다섯 경로를 직접 구현한다. 
한 가지를 구현할 때마다 같은 명령으로 통과한 개수가 느는지 본다.

5. 일곱 개가 통과하면 기본 `pytest`로 기존 테스트까지 모두 통과하는지 확인한다.
6. 내 구현을 `reading_api_mine.py`로 사본 보관한다.
LLM에 같은 요구사항과 테스트를 주어 `reading_api.py` 전체를 받고,
같은 테스트를 그대로 실행해 비교한다.
'''

class bookadd(BaseModel):
    title: str = Field(min_length=1)
    pages: int

class booksupdata(BaseModel):
    title: str
    pages: int
    read: bool

def books_id_find(books_id):
    for book_id in BOOKS:
        if book_id["id"] == books_id:
            return book_id
    raise HTTPException(status_code=404, detail="책을 찾을 수 없습니다")

@app.post("/books", status_code=201)
def book_add(data: bookadd):
    global NEXT_ID    
    books = {"id": NEXT_ID, "title": data.title, "pages": data.pages, "read": False}
    BOOKS.append(books)
    NEXT_ID += 1
    return books

@app.get("/books")
def books_list_all():
    return BOOKS

@app.get("/books/{book_id}")
def get_books(book_id: int):
    return books_id_find(book_id)
        
    
@app.put("/books/{book_id}")
def books_updata(book_id: int, data: booksupdata):
    book = books_id_find(book_id)
    book["title"] = data.title
    book["pages"] = data.pages
    book["read"] = data.read
    return book

@app.delete("/books/{book_id}")
def books_del(book_id: int):
    book = books_id_find(book_id)
    BOOKS.remove(book)
    return {"deleted" : book_id}