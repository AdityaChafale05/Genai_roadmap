# Chat Bot ( no memory )
import httpx
import os 
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("api_groq")

def ask_groq (question):
    
    response = httpx.post (
        "https://api.groq.com/openai/v1/chat/completions",
        headers ={"Authorization":f"Bearer {api_key}"},
        json = {
            "model" :"llama-3.1-8b-instant",
            "messages":[{"role":"user" ,"content":question}],
            "max_tokens":100
        }
    )
    
    if response.status_code == 200 :
        data = response.json()
        
        reply= data["choices"][0]["message"]["content"]   # don't forget that only 1 message is the output so only use "message"   not "messages"
        token_usage = data["usage"]["total_tokens"]
        
        return f"\nBy Groq : {reply} (Tokens used: {token_usage})"
        
    else:
        return f"Something went wrong: {response.status_code} {response.text}"
        
        

ask = input("Ask to groq :")
result = ask_groq(ask)        
print(result)