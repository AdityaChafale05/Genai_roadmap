
##  Simple storage of conversation in a local JSON file for persistent memory.


import os
import json
import httpx
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("api_groq")
MEMORY_FILE = "main_memory.json"

if os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "r") as f:
        try:
            conversation1 = json.load(f)
            print(f" Loaded {len(conversation1)} past messages from '{MEMORY_FILE}'.")
        except json.JSONDecodeError:
            print(" Memory file was corrupted/empty. Starting fresh.")
            conversation1 = []
else:
    print(" No previous memory found. Starting fresh conversation.")
    conversation1 = []
    
def ask_groq(messages):
    """Sends full conversation list to Groq."""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": messages
    }
    
    try:
        response = httpx.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"], result.get("usage", {})
        else:
            print(f"API Error {response.status_code}: {response.text}")
            return None, None
    except Exception as e:
        print(f"Network/Request Error: {e}")
        return None, None

def save_memory(conversation):
    """Saves the conversation list to disk."""
    with open(MEMORY_FILE, "w") as f:
        json.dump(conversation, f, indent=2)

# --- Main Chat Loop ---
print("\n--- Persistent Main Chat (Type 'exit' to quit) ---")

while True:
    user_input = input("\nYou: ").strip()
    
    if not user_input:
        continue
        
    if user_input.lower() == 'exit':
        print("Goodbye!")
        break

    # Append user input
    conversation1.append({"role": "user", "content": user_input})
    
    # Get reply
    reply, usage = ask_groq(conversation1)
    
    if reply:
        print(f"\nAssistant: {reply}")
        # Append assistant reply
        conversation1.append({"role": "assistant", "content": reply})
        
        # --- 2. Save memory after every successfully completed turn ---
        save_memory(conversation1)
    else:
        # Remove user message if the call failed so state stays clean
        conversation1.pop()
        print("\nFailed to get response. Message not saved.")                