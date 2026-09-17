from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')  # small, fast, well-known starter model

text = "I live in India"
embedding = model.encode(text)

"print(embedding) "
"print(len(embedding)) "


text1 = "I live in India"
text2 = "I reside in India"        # similar meaning, different words
text3 = "Pizza is my favorite food"  # unrelated meaning

emb1 = model.encode(text1)
emb2 = model.encode(text2)
emb3 = model.encode(text3)

similarity1 = model.similarity(emb1, emb2)  # should be high
similarity2 = model.similarity(emb1, emb3)  # should be low

print("\nSimilarities:")
print(f"Similarity between '{text1}' and '{text2}': {similarity1}")
print(f"Similarity between '{text1}' and '{text3}': {similarity2}")