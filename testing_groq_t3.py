# Chat Bot ( Adding memory  )
import httpx
import os 
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("api_groq")

def ask_groq (conversation):
    
    response = httpx.post (
        "https://api.groq.com/openai/v1/chat/completions",
        headers ={"Authorization":f"Bearer {api_key}"},
        json = {
            "model" :"llama-3.1-8b-instant",
            "messages": conversation,
            "max_tokens":100
        }
    )
    
    if response.status_code == 200 :
        data = response.json()
        
        reply= data["choices"][0]["message"]["content"]   # don't forget that only 1 message is the output so only use "message"   not "messages"
        token_usage = data["usage"]["total_tokens"]
        
        return reply,token_usage
        
    else:
        return None,None
        
        


conversation = []

while True :
    user_input = input("You: ")
    m1 = {"role": "user" , "content": user_input}
    conversation.append(m1)
    
    reply,token_usage = ask_groq(conversation)
    
    if (reply,token_usage) == (None, None):
        print("Error Occured")
        continue
    else:
        m2 = {"role": "assistant" , "content": reply}
        conversation.append(m2)
        print(f"Groq: {reply} (Tokens: {token_usage})")
        
        