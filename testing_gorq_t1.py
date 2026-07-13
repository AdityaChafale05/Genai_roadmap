
import httpx
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("api_groq")

response = httpx.post (
    "https://api.groq.com/openai/v1/chat/completions",
    headers = {"Authorization" :f"Bearer {api_key}"},
    
    json ={
        "model" :"llama-3.1-8b-instant",
        "messages":[{"role":"user","content":"what is a fun fact about pikachu"}],
        "max_tokens":100
    }
)

if response.status_code == 200 :
    data = response.json()
    reply = data["choices"][0]['message']['content']
    token_usage = data['usage']['total_tokens']
    
    print("By Gork :",reply)
    print("Token Usage :",token_usage)
    
    
else:
    print("something went wrong : " ,response.status_code,response.text)
    
        