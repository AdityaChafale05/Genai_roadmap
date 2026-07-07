from fastapi import FastAPI 
from pydantic import BaseModel

app = FastAPI()

class Person(BaseModel):
    name: str

@app.post("/greet")
def greet(person: Person):
    return {"message": f"Hello, {person.name}! Welcome to the world of APIs."}