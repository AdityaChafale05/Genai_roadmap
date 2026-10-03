

from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')  # small, fast, well-known starter model

memory_test = []


def compute_value(text):
    emb1 = model.encode(text)
    rank = []
    
    for item in memory_test:
        score = model.similarity(emb1, item["embedding"]).item()
        rank.append({"score": score, "text": item["text"]})
        
    sorted_rank = sorted( rank , key = lambda x : x["score"], reverse= True) 
    top_3 = sorted_rank[:3]
       
    return top_3




def save_memory(text):
    # Implementation for saving memory
    embedding = model.encode(text)
    memory_test.append({"text":text, "embedding": embedding})


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



"""
chat = input("Enter your text: ")
save_memory(chat)
         
result = compute_value(chat)

print("Top 3 similar texts:")
for item in result:
    print(f"- {item['text']} (score: {item['score']})")
"""

chat = input("Enter your query: ")

result = compute_value(chat)

print("\nTop 3 similar texts:")

for i, item in enumerate(result, 1):
    print(f"{i}. {item['text']}")
    print(f"   Score: {item['score']:.4f}")