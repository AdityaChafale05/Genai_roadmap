"""
Code for Groq API    ヾ(⌐■_■)ノ♪

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
    
    
"""

"""
ヾ(⌐■_■)ノ♪

Below code is for Gemini API - ( change models as they might not work )  

import httpx 
import os
from dotenv import load_dotenv

load_dotenv()
api = os.getenv("api_gemini")

response = httpx.post (
    "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent",
    
    headers={"x-goog-api-key": api},
    
    json={
        "contents": [
            {"parts": [{"text": "Tell me a joke about college, relatable to students"}]}
        ]
    },
    timeout=30.0
)

if response.status_code == 200 :
    data = response.json()
    
    reply = data["candidates"][0]["content"]["parts"][0]["text"]
    token_usage = data["usageMetadata"]["totalTokenCount"]
    print(reply)
    print("Token Usage:", token_usage)
else:
    print("Something went wrong:" ,response.status_code, response.text)    
    

"""


"""
TO check the available models in Gemini API

import httpx
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("api_gemini")

response = httpx.get(
    "https://generativelanguage.googleapis.com/v1beta/models",
    headers={"x-goog-api-key": api_key},
    timeout=30.0
)

if response.status_code == 200:
    data = response.json()
    for model in data["models"]:
        print(model["name"])
else:
    print("Something went wrong:", response.status_code, response.text)
    
"""