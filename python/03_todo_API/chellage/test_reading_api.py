# from fastapi.testclient import TestClient
# from reading_api import app, BOOKS

# client = TestClient(app)

# def test_create_books():
#     BOOKS.clear()
#     response = client.post("/books", json={"title": "가나다", "pages" : 200})
#     assert response.status_code == 201
#     book = response.json()
#     assert book["title"] == "가나다"
#     assert book["pages"] == 200
#     assert book["read"] is False


# def test_id_list():
#     BOOKS.clear()
#     book = client.post("/todos", json={"tilte": "ASDF","pages":10}).json()
#     assert client.get("/todos").json() == [book]
#     assert client.get("/todos/" + str(book["id"])).json() == book
from fastapi.testclient import TestClient
from reading_api import app, BOOKS

client = TestClient(app)

def test_create_and_list_books():
    """등록과 목록 조회: 201이고 title, pages가 요청한 값이며 read는 false다. 목록에 그 책이 있다."""
    BOOKS.clear()
    
    # 1. 등록 (POST)
    response = client.post("/books", json={"title": "파이썬 입문", "pages": 320})
    assert response.status_code == 201
    
    data = response.json()
    assert data["title"] == "파이썬 입문"
    assert data["pages"] == 320
    assert data["read"] is False
    
    book_id = data["id"]

    # 2. 목록 조회 (GET)
    list_response = client.get("/books")
    assert list_response.status_code == 200
    books_list = list_response.json()
    assert len(books_list) == 1
    assert books_list[0]["id"] == book_id
    assert books_list[0]["title"] == "파이썬 입문"


def test_get_single_book():
    """단건 조회: 등록 응답의 id로 조회하면 같은 책이 반환된다."""
    BOOKS.clear()
    
    res = client.post("/books", json={"title": "자바스크립트 완벽 가이드", "pages": 500})
    book_id = res.json()["id"]

    # 단건 조회 (GET)
    response = client.get(f"/books/{book_id}")
    assert response.status_code == 200
    book = response.json()
    assert book["id"] == book_id
    assert book["title"] == "자바스크립트 완벽 가이드"
    assert book["pages"] == 500


def test_book_not_found():
    """존재하지 않는 id: 404이고 detail이 책을 찾을 수 없습니다다."""
    BOOKS.clear()
    
    response = client.get("/books/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "책을 찾을 수 없습니다"


def test_update_book():
    """수정: 수정 응답과 다시 조회한 값이 요청한 세 값과 같다."""
    BOOKS.clear()
    
    res = client.post("/books", json={"title": "리팩토링", "pages": 400})
    book_id = res.json()["id"]

    # 수정 (PUT) - title, pages, done(또는 read) 세 값 전달
    update_data = {"title": "리팩토링 2판", "pages": 450, "read": True}
    update_res = client.put(f"/books/{book_id}", json=update_data)
    assert update_res.status_code == 200
    
    updated_book = update_res.json()
    assert updated_book["title"] == "리팩토링 2판"
    assert updated_book["pages"] == 450
    assert updated_book["read"] is True

    # 다시 조회해서 확인
    get_res = client.get(f"/books/{book_id}")
    fetched_book = get_res.json()
    assert fetched_book["title"] == "리팩토링 2판"
    assert fetched_book["pages"] == 450
    assert fetched_book["read"] is True


def test_delete_and_id_generation():
    """삭제와 id 발급: 삭제 후 조회는 404다. 그 뒤 새로 등록한 책의 id가 남은 책과 중복되지 않는다."""
    BOOKS.clear()
    
    # 책 두 권 등록 (id 1, 2)
    b1 = client.post("/books", json={"title": "책1", "pages": 100}).json()
    b2 = client.post("/books", json={"title": "책2", "pages": 200}).json()
    
    # 첫 번째 책 삭제 (DELETE)
    del_res = client.delete(f"/books/{b1['id']}")
    assert del_res.status_code == 200

    # 삭제된 책 조회 시 404 확인
    assert client.get(f"/books/{b1['id']}").status_code == 404

    # 새로 책 등록했을 때 기존 남은 책(b2)의 id와 중복되지 않고 새로 발급되는지 확인
    b3 = client.post("/books", json={"title": "책3", "pages": 300}).json()
    assert b3["id"] != b1["id"]
    assert b3["id"] != b2["id"]


def test_validation_title():
    """title 검증: 누락됐을 때와 빈 문자열일 때 모두 422다."""
    BOOKS.clear()
    
    # 1. title 누락
    res_missing = client.post("/books", json={"pages": 100})
    assert res_missing.status_code == 422

    # 2. title이 빈 문자열
    res_empty = client.post("/books", json={"title": "", "pages": 100})
    assert res_empty.status_code == 422


def test_validation_pages():
    """pages 검증: 누락됐을 때와 정수로 변환할 수 없는 값일 때 모두 422다."""
    BOOKS.clear()
    
    # 1. pages 누락
    res_missing = client.post("/books", json={"title": "테스트북"})
    assert res_missing.status_code == 422

    # 2. 정수로 변환할 수 없는 값("많음")
    res_invalid = client.post("/books", json={"title": "테스트북", "pages": "많음"})
    assert res_invalid.status_code == 422