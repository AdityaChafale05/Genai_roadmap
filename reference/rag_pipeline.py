
"""
I used a small local embedding model for speed/cost reasons 
— it correctly finds topically-related content, 
but has real precision limits on subtler intent like specific verbs. 
This is a known tradeoff with lightweight embedding models,
and a larger model (or a hosted one like Gemini's) would likely improve this at the cost of speed/quota.
"""


from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')  
memory_test = []


def compute_value(text,top_n=3):
    emb1 = model.encode(text)
    rank = []
    
    for item in memory_test:
        score = model.similarity(emb1, item["embedding"]).item()
        rank.append({"score": score, "text": item["text"]})
        
    sorted_rank = sorted( rank , key = lambda x : x["score"], reverse= True) 
    return sorted_rank[:top_n]  


def save_memory(text):
    embedding = model.encode(text)
    memory_test.append({"text":text, "embedding": embedding})


if __name__ == "__main__":
    memories = [
        "I live in Mumbai.",
        "I love playing football on weekends.",
        "My favorite programming language is Python.",
        "I am learning FastAPI for backend development.",
        "I use Fedora Linux on my laptop.",
        "I enjoy building AI applications.",
        "My favorite food is pizza.",
        "I am learning React and Tailwind CSS.",
        "I want to build a chatbot with memory.",
        "I like programming in Python.",
        "Python is my favorite programming language.",
        "I moved to Pune."
    ]
    for memory in memories:
        save_memory(memory)



    chat = input("Enter your query: ")
    result = compute_value(chat, top_n=3)
    
    print("\nTop 3 similar texts:")
    for i, item in enumerate(result, 1):
        print(f"{i}. {item['text']}")
        print(f"   Score: {item['score']:.4f}")
 