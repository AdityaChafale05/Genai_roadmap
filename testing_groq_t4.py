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
        

# the subchat ( with memory )

def ask_subchat ( question ,main):
    history_text = ""
    
    for msg in main :
        history_text += f" {msg['role']} : {msg['content']} \n"
        
    conversation2 = [
        {"role": "user", "content": f"Background:\n{history_text}\nQuestion: {question}"}
    ]
    reply, tokens = ask_groq(conversation2)
    return reply, tokens


conversation1 = []

while True :
    user_input = input("ヾ(⌐■_■)ノ♪  You: ")
    m1 = {"role": "user" , "content": user_input}
    conversation1.append(m1)
    
    reply,token_usage = ask_groq(conversation1)
    
    if (reply,token_usage) == (None, None):
        print("Error Occured")
        continue
    
    # try again ( correct)
    elif user_input == 'sub' :
        
        print("Arrived in Sub-Chat -- type 'exit' to return to main chat :\n")
        
        while True:
            sub_question = input("Sub-chat, ask your question: ")
            
            if sub_question == 'exit':
                print("Returning to main chat ...")
                break
            
            reply, tokens = ask_subchat(sub_question, conversation1)
            print(f"Sub-chat answer: {reply} (Tokens: {tokens})")
    
    
    else:
        m2 = {"role": "assistant" , "content": reply}
        conversation1.append(m2)
        print(f"✧(ↀ_ↀ) Groq: {reply} (Tokens: {token_usage})")
        
        