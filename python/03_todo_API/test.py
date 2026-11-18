# class Animal:
#     def hello(self):
#         print("안녕")


# class Dog(Animal):
#     pass


# dog = Dog()
# dog.hello()

# from pydantic import BaseModel

# class TodoCreate(BaseModel):
#     text: str

# todo = TodoCreate(text="산책하기")
# print(todo)
# print(todo.text)

# wrong = TodoCreate(text=123)
# print("이 줄은 실행되지 않는다")