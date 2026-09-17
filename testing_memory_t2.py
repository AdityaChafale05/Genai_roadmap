
## 


from urllib import response

import httpx
import os 
from dotenv import load_dotenv
import json

from testing_memory_t1 import MEMORY_FILE

load_dotenv()
api_key = os.getenv("api_groq")
main_file = "main.json"

if os.path.exists(main_file):
    with open(main_file, "r") as f:
        try:
            conversation1 = json.load(f)
            print(f" Loaded {len(conversation1)} past messages from '{main_file}'.")
        except json.JSONDecodeError:
            print(" Memory file was corrupted/empty. Starting fresh.")
            conversation1 = []
else:
    print(" No previous memory found. Starting fresh conversation.")
    conversation1 = []


def ask_groq (conversation):
    
    response = httpx.post (
        "https://api.groq.com/openai/v1/chat/completions",
        headers ={"Authorization":f"Bearer {api_key}","Content-Type": "application/json"},
        json = {
            "model" :"llama-3.1-8b-instant",
            "messages": conversation,
            "max_tokens":100
        }
    )
    
    try :
        if response.status_code == 200 :
            data = response.json()
        
            reply= data["choices"][0]["message"]["content"]   # don't forget that only 1 message is the output so only use "message"   not "messages"
            token_usage = data["usage"]["total_tokens"]
        
            return reply,token_usage
        
        
        else:
            return None,None
        
    except Exception as e:
            print(f"Network/Request Error: {e}")
            return None, None
        
        
def save_memory(conversation):
    """Saves the conversation list to disk."""
    with open(main_file, "w") as f:
        json.dump(conversation, f, indent=2)

        
        
        
def ask_subchat ( question ,main):
    history_text = ""
    
    for msg in main :
        history_text += f" {msg['role']} : {msg['content']} \n"
        
    conversation2 = [
        {"role": "user", "content": f"Background:\n{history_text}\nQuestion: {question}"}
    ]
    reply, tokens = ask_groq(conversation2)
    return reply, tokens
        
        
while True :
    user_input = input("ヾ(⌐■_■)ノ♪  You: ")
    m1 = {"role": "user" , "content": user_input}
    conversation1.append(m1)
    
    reply,token_usage = ask_groq(conversation1)        