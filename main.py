
"""
from fastapi import FastAPI 
from pydantic import BaseModel

app = FastAPI()

class Person(BaseModel):
    name: str

@app.post("/greet")
def greet(person: Person):
    return {"message": f"Hello, {person.name}! Welcome to the world of APIs."}
"""
import httpx, os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("api_groq")

response = httpx.get(
    "https://api.groq.com/openai/v1/models",
    headers={"Authorization": f"Bearer {api_key}"}
)
data = response.json()
for m in data["data"]:
    print(m["id"])