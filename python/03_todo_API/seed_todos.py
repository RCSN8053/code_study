import requests

url = "http://127.0.0.1:8000/todos"
before = requests.get(url).json()
print("등록 전", len(before))

for text in ["물 마시기", "책 읽기"]:
    response = requests.post(url, json={"text": text})
    print(response.status_code, response.json())

after = requests.get(url).json()
print("등록 후", len(after))
print("늘어난 수", len(after) - len(before))
