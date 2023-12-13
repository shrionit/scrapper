from fastapi import FastAPI
from models import DBSession

api = FastAPI()


@api.get("/hello")
def greet():
    {"result": "Hello From API"}
