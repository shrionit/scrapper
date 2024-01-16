from pydantic import BaseModel


class Person(BaseModel):
    name: str
    age: int


def main() -> None:
    person1 = Person(name="hello", age=44)
    print(person1)


if __name__ == "__main__":
    main()
