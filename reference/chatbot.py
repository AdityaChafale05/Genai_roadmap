import os
import json
import httpx
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("api_groq")
MEMORY_FILE = "main_memory.json"

# --- Load main chat memory ---
if os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "r") as f:
        try:
            conversation1 = json.load(f)
            print(f"Loaded {len(conversation1)} past messages from '{MEMORY_FILE}'.")
        except json.JSONDecodeError:
            print("Memory file was corrupted/empty. Starting fresh.")
            conversation1 = []
else:
    print("No previous memory found. Starting fresh conversation.")
    conversation1 = []

# --- NEW: bookmark tracking how much of conversation1 sub-chat has already seen ---
last_seen_index = 0


def ask_groq(messages):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "openai/gpt-oss-20b",
        "messages": messages,
        "max_tokens": 250
    }
    try:
        response = httpx.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            reply = result["choices"][0]["message"]["content"]
            tokens = result["usage"]["total_tokens"]
            return reply, tokens
        else:
            print(f"API Error {response.status_code}: {response.text}")
            return None, None
    except Exception as e:
        print(f"Network/Request Error: {e}")
        return None, None


def save_memory(conversation):
    with open(MEMORY_FILE, "w") as f:
        json.dump(conversation, f, indent=2)


# --- NEW: ask_subchat now takes start_index, only sends NEW main-chat messages ---
def ask_subchat(question, main, start_index):
    new_messages = main[start_index:]
    print(f"[DEBUG] Sub-chat received {len(new_messages)} new message(s) starting from index {start_index}")
    history_text = ""
    for msg in new_messages:
        history_text += f"{msg['role']}: {msg['content']}\n"

    conversation2 = [
        {"role": "user", "content": f"Background:\n{history_text}\nQuestion: {question}"}
    ]
    reply, tokens = ask_groq(conversation2)
    return reply, tokens


# --- Main Loop ---
print("\n--- Chat (type 'sub' for sub-chat, 'exit' to quit) ---")

while True:
    user_input = input("\n ヾ(⌐■_■)ノ♪ You: ").strip()
    if not user_input:
        continue
    if user_input.lower() == 'exit':
        print("Goodbye!")
        break

    elif user_input.lower() == 'sub':
        sub_question = input("Sub-chat, ask your question: ")
        reply, tokens = ask_subchat(sub_question, conversation1, last_seen_index)
        if reply:
            print(f"Sub-chat: {reply} (Tokens: {tokens})")
        else:
            print("Sub-chat request failed.")
        last_seen_index = len(conversation1)   # NEW: update bookmark after sub-chat use
        continue

    conversation1.append({"role": "user", "content": user_input})
    reply, usage = ask_groq(conversation1)
    if reply:
        print(f"\n ✧(ↀ_ↀ)  Assistant: {reply}")
        conversation1.append({"role": "assistant", "content": reply})
        save_memory(conversation1)
    else:
        conversation1.pop()
        print("\nFailed to get response. Message not saved.")